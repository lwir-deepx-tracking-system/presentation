from pathlib import Path
root=Path('/tmp/lwir-perf-20261116')
p=root/'source/src/camera/camera.cpp'
s=p.read_text()
insert=r'''
#include <cstdlib>
#include <fstream>
#include <stdexcept>
#include <vector>

namespace {
// Experiment-only source: preload actual CV_16UC1 camera frames, then pace without file I/O.
struct ReplaySource {
  std::vector<cv::Mat> images;
  struct Release { long long planned, actual; };
  std::vector<Release> releases;
  std::size_t index=0;
  std::chrono::steady_clock::time_point next;
  std::chrono::steady_clock::duration period{};
  bool enabled=false;
} replay;
}
'''
s=s.replace('Camera::~Camera()',insert+'\nCamera::~Camera()')
s=s.replace('  // STEP 1: Scan for connected devices until one is available.',r'''
  if (const char* folder=std::getenv("LWIR_REPLAY_DIR")) {
    const char* rate=std::getenv("LWIR_REPLAY_FPS");
    const double fps=rate?std::stod(rate):30.0;
    if (!(fps>0 && fps<=1000)) throw std::runtime_error("invalid replay FPS");
    replay=ReplaySource{};
    for (int i=1;i<=20;++i) {
      auto img=cv::imread(std::string(folder)+"/"+std::to_string(i)+".png",cv::IMREAD_UNCHANGED);
      if(img.empty()||img.type()!=CV_16UC1||img.cols!=640||img.rows!=480)
        throw std::runtime_error("replay needs actual 640x480 CV_16UC1 frames");
      replay.images.push_back(std::move(img));
    }
    replay.releases.reserve(20000);
    replay.period=std::chrono::duration_cast<std::chrono::steady_clock::duration>(std::chrono::duration<double>(1.0/fps));
    replay.next=std::chrono::steady_clock::now();
    replay.enabled=true;width_=640;height_=480;
    Logger::info("[Replay] actual-frame memory replay FPS="+std::to_string(fps));
    return true;
  }
  // STEP 1: Scan for connected devices until one is available.''')
s=s.replace('  if(!te_ || width_ <= 0 || height_ <= 0)',r'''
  if(replay.enabled) {
    const auto planned=replay.next;
    std::this_thread::sleep_until(planned);
    replay.images[replay.index++%replay.images.size()].copyTo(frame.image);
    const auto actual=std::chrono::steady_clock::now();
    replay.releases.push_back({std::chrono::duration_cast<std::chrono::nanoseconds>(planned.time_since_epoch()).count(),
      std::chrono::duration_cast<std::chrono::nanoseconds>(actual.time_since_epoch()).count()});
    replay.next+=replay.period;
    return true;
  }
  if(!te_ || width_ <= 0 || height_ <= 0)''')
s=s.replace('  if(!te_)\n    return;',r'''
  if(replay.enabled) {
    if(const char* folder=std::getenv("LWIR_PERF_DIR")) {
      std::ofstream out(std::string(folder)+"/replay-source.csv");
      out<<"planned_ns,actual_ns\n";
      for(const auto& r:replay.releases) out<<r.planned<<','<<r.actual<<'\n';
    }
    replay=ReplaySource{};width_=0;height_=0;
    return;
  }
  if(!te_)
    return;''')
p.write_text(s)
# Preserve the original runner and tag this experiment separately.
p=root/'runner.py';s=p.read_text();s=s.replace("m={'case':case", "m={'input_source':'actual-camera-memory-replay','requested_fps':float(os.environ.get('LWIR_REPLAY_FPS','0')),'case':case")
p.write_text(s)
