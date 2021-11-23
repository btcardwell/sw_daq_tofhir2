#!/usr/bin/env python

import os
import argparse

parser = argparse.ArgumentParser(description='convert raw data')
parser.add_argument("--config", type=str, required=True, help="Configuration file")
parser.add_argument("-r", type=str, dest="run", required=True, help = "Run number")
parser.add_argument("--mode", type=str, required=True, choices=["r", "s", "c", "e"], help = "reconstruction mode (singles, coincicences or event)")
parser.add_argument("--refChannel", type=str, required=False, help = "reference channel")
parser.add_argument("--pedestals", dest="pedestals", action="store_true", help="Enable the acquisition of pedestals")

args = parser.parse_args()

if args.mode == 'r':
    command = "./convert_raw_to_raw --daqv1 --config "+args.config+" -i /home/data/mtd/data/tofhir2/raw/run"+args.run+".rawf -o /home/data/mtd/data/tofhir2/reco/run"+args.run+"_r.root"
    print(command)
    os.system(command)

if args.mode == 's':
    mainCommand = "./convert_raw_to_singles --daqv1 --config "+args.config+" -i /home/data/mtd/data/tofhir2/raw/run"+args.run+".rawf --writeRoot"
    if args.pedestals:
        command = "./convert_raw_to_singles --daqv1 --config "+args.config+" -i /home/data/mtd/data/tofhir2/raw/run"+args.run+"_ped1 -o /home/data/mtd/data/tofhir2/reco/run"+args.run+"_ped1_s.root --writeRoot"
        os.system(command)
        command = "./convert_raw_to_singles --daqv1 --config "+args.config+" -i /home/data/mtd/data/tofhir2/raw/run"+args.run+"_ped2 -o /home/data/mtd/data/tofhir2/reco/run"+args.run+"_ped2_s.root --writeRoot"
        os.system(command)
        command = "./analyze_pedestals.exe /home/data/mtd/data/tofhir2/reco/run"+args.run+"_ped1_s.root /home/data/mtd/data/tofhir2/reco/run"+args.run+"_ped2_s.root /home/data/mtd/data/tofhir2/reco/run"+args.run+"_pedestals.root"
        os.system(command)
        mainCommand += " --pedestals -o /home/data/mtd/data/tofhir2/reco/run"+args.run+"_ped_s.root"
    else:
        mainCommand += " -o /home/data/mtd/data/tofhir2/reco/run"+args.run+"_s.root"
    print(mainCommand)
    os.system(mainCommand)

if args.mode == 'c':
    command = "./convert_raw_to_coincidence --daqv1 --config "+args.config+" -i /home/data/mtd/data/tofhir2/raw/run"+args.run+".rawf -o /home/data/mtd/data/tofhir2/reco/run"+args.run+"_c.root --writeRoot"
    os.system(command)

if args.mode == 'e':
    mainCommand = "./convert_raw_to_event --daqv1 --config "+args.config+" -i /home/data/mtd/data/tofhir2/raw/run"+args.run+".rawf --writeRoot"
    if args.pedestals:
        command = "./convert_raw_to_singles --daqv1 --config "+args.config+" -i /home/data/mtd/data/tofhir2/raw/run"+args.run+"_ped1 -o /home/data/mtd/data/tofhir2/reco/run"+args.run+"_ped1_s.root --writeRoot"
        os.system(command)
        command = "./convert_raw_to_singles --daqv1 --config "+args.config+" -i /home/data/mtd/data/tofhir2/raw/run"+args.run+"_ped2 -o /home/data/mtd/data/tofhir2/reco/run"+args.run+"_ped2_s.root --writeRoot"
        os.system(command)
        command = "./analyze_pedestals.exe /home/data/mtd/data/tofhir2/reco/run"+args.run+"_ped1_s.root /home/data/mtd/data/tofhir2/reco/run"+args.run+"_ped2_s.root /home/data/mtd/data/tofhir2/reco/run"+args.run+"_pedestals.root"
        os.system(command)
        mainCommand += " --pedestals -o /home/data/mtd/data/tofhir2/reco/run"+args.run+"_ped_e.root"
    else:
        mainCommand += " -o /home/data/mtd/data/tofhir2/reco/run"+args.run+"_e.root"
    if args.refChannel :
        mainCommand += " --refChannel "+args.refChannel
    print(mainCommand)
    os.system(mainCommand)
