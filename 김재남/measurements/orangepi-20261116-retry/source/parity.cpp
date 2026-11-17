#include <filesystem>
#include <fstream>
#include <future>
#include <iostream>
#include <opencv2/imgcodecs.hpp>
#include "config/app_config.hpp"
#include "detection/detector_factory.hpp"
// 실제 저장한 카메라 프레임을 같은 파이프라인에 넣어 검출 결과를 보존한다.
int main(int argc,char** argv) {
    if(argc!=5) return 2;
    try {
        auto config=load_model_config(argv[1]);
        DetectionConfig inference; inference.max_inflight=1; inference.buffer_count=6;
        inference.use_ort=std::string(argv[3])=="1";
        auto factory=DetectorFactory::for_model(config);auto pipeline=factory->create(config,inference);
        std::ofstream output(argv[4]);output<<"frame_id,class_id,x,y,width,height,confidence\n";output.precision(10);
        for(unsigned i=1;i<=20;++i) {
            auto frame=std::make_shared<FrameContext>();frame->metadata.frame_id=i;
            frame->image=cv::imread(std::string(argv[2])+"/"+std::to_string(i)+".png",cv::IMREAD_UNCHANGED);
            if(frame->image.empty()) throw std::runtime_error("missing real camera sample");
            std::promise<std::vector<Detection>> promise;auto future=promise.get_future();
            pipeline->submit_async(frame,[&](std::vector<Detection> d,std::exception_ptr error,DetectionTiming) {
                if(error) promise.set_exception(error);else promise.set_value(std::move(d));
            });
            auto detections=future.get();pipeline->wait_idle();
            for(const auto& d:detections)output<<i<<','<<d.class_id<<','<<d.x<<','<<d.y<<','<<d.width<<','<<d.height<<','<<d.confidence<<'\n';
        }
        pipeline->wait_idle();return output ? 0:3;
    } catch(const std::exception& e) { std::cerr<<e.what()<<'\n';return 1; }
}
