#include "ProcessHit.hpp"
#include <math.h>
using namespace PETSYS;

ProcessHit::ProcessHit(SystemConfig *systemConfig, EventStream *eventStream, EventSink<Hit> *sink) :
OverlappedEventHandler<RawHit, Hit>(sink), systemConfig(systemConfig), eventStream(eventStream)
{
	nReceived = 0;
	nReceivedInvalid = 0;
	nTDCCalibrationMissing = 0;
	nQDCCalibrationMissing = 0;
	nXYZMissing = 0;
	nEnergyCalibrationMissing = 0;
	nSent = 0;
}

EventBuffer<Hit> * ProcessHit::handleEvents (EventBuffer<RawHit> *inBuffer)
{
	// TODO Add instrumentation
	unsigned N =  inBuffer->getSize();

	EventBuffer<Hit> * outBuffer = new EventBuffer<Hit>(N, inBuffer);

	int triggerID = eventStream->getTriggerID();

	bool useTDC = systemConfig->useTDCCalibration();
	bool useQDC = systemConfig->useQDCCalibration();
	bool useEnergyCal = systemConfig->useEnergyCalibration();
	bool useXYZ = systemConfig->useXYZ();
	//intf("%d\n", N);
	uint32_t lReceived = 0;
	uint32_t lReceivedInvalid = 0;
	uint32_t lTDCCalibrationMissing = 0;
	uint32_t lQDCCalibrationMissing = 0;
	uint32_t lEnergyCalibrationMissing = 0;
	uint32_t lXYZMissing = 0;
	uint32_t lSent = 0;
	
	for(int i = 0; i < N; i++) {
		RawHit &in = inBuffer->get(i);
		Hit &out = outBuffer->getWriteSlot();
		out.raw = &in;
		
		uint8_t eventFlags = in.valid ? 0x0 : 0x1;
		
		if((in.channelID >> 11) == triggerID) {
			// This event comes from the trigger
			// TODO Check that this works with TOFHiR 2 firmware
			out.time = in.time;
			out.time -= (in.t1fine - 27) * 0.25;
			out.timeEnd = out.time;
			out.energy = (in.t2fine == 28) ? 1 : -1;
			out.region = -1;
			out.x = out.y = out.z = 0.0;
			out.xi = out.yi = 0;
		}
		else {
	      		
			SystemConfig::ChannelConfig &cc = systemConfig->getChannelConfig(in.channelID);
			SystemConfig::TacConfig &ct = cc.tac_T[in.tacID];
			SystemConfig::TacConfig &ce = cc.tac_E[in.tacID];
			SystemConfig::QacConfig &cq = cc.qac_Q[in.tacID];
			SystemConfig::EnergyConfig &cen = cc.eCal[in.tacID];
			
			out.time = in.time;
			if(useTDC) {
				float q_T1 = ( -ct.a1 + sqrtf((ct.a1 * ct.a1) - (4.0f * (ct.a0 - in.t1fine) * ct.a2))) / (2.0f * ct.a2) ;
				out.time = double(in.time) - q_T1 - ct.t0;
				out.qT1 = q_T1;
				if(ct.a1 == 0) eventFlags |= 0x2;
			}
			
			out.timeEnd = in.timeEnd;
			if(useTDC) {
				float q_T2 = ( -ce.a1 + sqrtf((ce.a1 * ce.a1) - (4.0f * (ce.a0 - in.t2fine) * ce.a2))) / (2.0f * ce.a2) ;
				out.timeEnd = double(in.timeEnd) - q_T2 - ce.t0;
				out.qT2 = q_T2;
				if(ce.a1 == 0) eventFlags |= 0x2;
			}
			out.energy = out.timeEnd - out.time; 
			
			out.energy = in.qfine;
			if(useQDC) {
			
				// Calculate the event's integration time
				float ti = double(in.timeEndQ) - out.time;
				
				// Calculate the pedestal from the polynomial
				float pedestal = 
					cq.p0 +
					cq.p1 * ti +
					cq.p2 * ti * ti +
					cq.p3 * ti * ti * ti +
					cq.p4 * ti * ti * ti * ti +
					cq.p5 * ti * ti * ti * ti * ti +
					cq.p6 * ti * ti * ti * ti * ti * ti +
					cq.p7 * ti * ti * ti * ti * ti * ti * ti +
					cq.p8 * ti * ti * ti * ti * ti * ti * ti * ti +
					cq.p9 * ti * ti * ti * ti * ti * ti * ti * ti * ti;

				// Subtract the pedestal from the ASIC's raw QDC measurement
				out.energy = in.qfine - pedestal;
				
				if(cq.p1 == 0) eventFlags |= 0x4;
		
			}
			
			out.region = -1;
			out.x = out.y = out.z = 0.0;
			out.xi = out.yi = 0;
			if(useXYZ) {
				out.region = cc.triggerRegion;
				out.x = cc.x;
				out.y = cc.y;
				out.z = cc.z;
				out.xi = cc.xi;
				out.yi = cc.yi;
				if(cc.triggerRegion == -1) eventFlags |= 0x8;
			}
			
		}
		
			lReceived += 1;
			if((eventFlags & 0x1) != 0) lReceivedInvalid += 1;
			if((eventFlags & 0x2) != 0) lTDCCalibrationMissing += 1;
			if((eventFlags & 0x4) != 0) lQDCCalibrationMissing += 1;
			if((eventFlags & 0x8) != 0) lXYZMissing += 1;
			if((eventFlags & 0x16) != 0) lEnergyCalibrationMissing += 1;

		if(eventFlags == 0) {
			out.valid = true;
			outBuffer->pushWriteSlot();
			lSent += 1;
		}
	}
	
	atomicAdd(nReceived, lReceived);
	atomicAdd(nReceivedInvalid, lReceivedInvalid);
	atomicAdd(nTDCCalibrationMissing, lTDCCalibrationMissing);
	atomicAdd(nQDCCalibrationMissing, lQDCCalibrationMissing);
	atomicAdd(nEnergyCalibrationMissing, lEnergyCalibrationMissing);	
	atomicAdd(nXYZMissing, lXYZMissing);
	atomicAdd(nSent, lSent);
	
	return outBuffer;
}

void ProcessHit::report()
{
	fprintf(stderr, ">> ProcessHit report\n");
	fprintf(stderr, " hits received\n");
	fprintf(stderr, "  %10u total\n", nReceived);
	fprintf(stderr, "  %10u (%4.1f%%) invalid\n", nReceivedInvalid, 100.0 * nReceivedInvalid / nReceived);
	fprintf(stderr, " hits dropped\n");
	fprintf(stderr, "  %10u (%4.1f%%) missing TDC calibration\n", nTDCCalibrationMissing, 100.0 * nTDCCalibrationMissing / nReceived);
	fprintf(stderr, "  %10u (%4.1f%%) missing QDC calibration\n", nQDCCalibrationMissing, 100.0 * nQDCCalibrationMissing / nReceived);
	if(systemConfig->useEnergyCalibration())
		fprintf(stderr, "  %10u (%4.1f%%) missing Energy calibration\n", nEnergyCalibrationMissing, 100.0 * nEnergyCalibrationMissing / nReceived);
	fprintf(stderr, "  %10u (%4.1f%%) missing XYZ information\n", nXYZMissing, 100.0 * nXYZMissing / nReceived);
	fprintf(stderr, " hits passed\n");
	fprintf(stderr, "  %10u (%4.1f%%)\n", nSent, 100.0 * nSent / nReceived);
	
	OverlappedEventHandler<RawHit, Hit>::report();
}
