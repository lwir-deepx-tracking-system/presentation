#include <i3system_TE.h>
#include <i3_types.h>
#include <chrono>
#include <vector>
#include <iostream>
#include <map>
// Measure SDK receive throughput alone, without inference, queues or file output.
int main(){i3::SCANINFO scan[MAX_USB_NUM]{};if(ScanTE(scan)!=1)return 1;int idx=-1;for(int i=0;i<MAX_USB_NUM;++i)if(scan[i].bDevCon==1){idx=i;break;}if(idx<0)return 2;auto*c=i3::OpenTE_A(idx);if(!c)return 3;std::vector<unsigned short>b(c->GetImageWidth()*c->GetImageHeight());c->SetShutterMode(I3_TEMP_SHUTTER);c->SetShutterTemperature(1);c->ShutterCalibrationOn();using C=std::chrono::steady_clock;for(bool agc:{true,false}){auto start=C::now();while(std::chrono::duration<double>(C::now()-start).count()<3)c->RecvImage(b.data(),agc);std::map<int,int>rc;start=C::now();while(std::chrono::duration<double>(C::now()-start).count()<15)++rc[c->RecvImage(b.data(),agc)];double seconds=std::chrono::duration<double>(C::now()-start).count();std::cout<<"agc="<<agc<<" seconds="<<seconds<<" fps="<<rc[1]/seconds;for(auto[k,v]:rc)std::cout<<" rc"<<k<<"="<<v;std::cout<<std::endl;}c->CloseTE();}
