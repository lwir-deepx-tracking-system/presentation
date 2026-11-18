#pragma once
// 실험 복사본 전용 계측. 실행 중에는 작은 이벤트만 보관하고 종료 후 CSV로 기록한다.
#include <chrono>
#include <cstdlib>
#include <cstdint>
#include <fstream>
#include <mutex>
#include <string>
#include <vector>
namespace perf_experiment {
using Clock = std::chrono::steady_clock;
inline long long ns(Clock::time_point t) { return std::chrono::duration_cast<std::chrono::nanoseconds>(t.time_since_epoch()).count(); }
struct Event { std::string stage; std::uint64_t id; long long capture,done; double a,b,c,d,e,f,g,h; };
class Recorder {
    std::mutex mutex_;
    std::vector<Event> events_;
    std::string root_;
public:
    Recorder() { if (const char* p = std::getenv("LWIR_PERF_DIR")) root_=p; events_.reserve(12000); }
    void record(const char* stage, std::uint64_t id, Clock::time_point captured,
        double a=0,double b=0,double c=0,double d=0,double e=0,double f=0,double g=0,double h=0) {
        if (root_.empty()) return;
        const auto done=ns(Clock::now());
        std::lock_guard<std::mutex> lock(mutex_);
        if (events_.size() >= 50000) std::abort();
        events_.push_back({stage,id,ns(captured),done,a,b,c,d,e,f,g,h});
        if (id==1 && std::string(stage)=="camera") { std::ofstream ready(root_+"/ready"); ready<<done; }
    }
    ~Recorder() {
        if (root_.empty()) return;
        std::ofstream out(root_+"/telemetry.csv");
        out<<"stage,frame_id,capture_ns,done_ns,preprocess_ms,latency_ms,postprocess_ms,npu_ms,input_format_us,output_format_us,cpu_task_us,cpu_valid\n";
        out.precision(12);
        for (const auto& e:events_) out<<e.stage<<','<<e.id<<','<<e.capture<<','<<e.done<<','<<e.a<<','<<e.b<<','<<e.c<<','<<e.d<<','<<e.e<<','<<e.f<<','<<e.g<<','<<e.h<<'\n';
    }
};
inline Recorder& recorder() { static Recorder r; return r; }
inline void record(const char* s,std::uint64_t id,Clock::time_point captured) { recorder().record(s,id,captured); }
}
