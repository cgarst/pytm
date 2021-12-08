#!/usr/bin/env python3

from pytm import (
    TM,
    Boundary,
    ExternalEntity,
    Process,
    Datastore,
    Dataflow,
    Classification,
    Data
)

tm = TM("Jurassic Park")
tm.description = "Jurassic Park Threat Model"

# Define core systems

silicon_graphics_fsn = Process("Silicon Graphics File System Navigator")
silicon_graphics_fsn.OS = "Unix"

file_server = Datastore("Park File Server")
file_server.OS = "Unix"
silicon_graphics_fsn_to_file_server = Dataflow(silicon_graphics_fsn, file_server, "Workstation File Server Access")
silicon_graphics_fsn_to_file_server.protocol = "NFS"
silicon_graphics_fsn_to_file_server.dstPort = 2049
silicon_graphics_fsn_to_file_server.data = Data('Complete park records', classification=Classification.TOP_SECRET)

park_security_system = Process("Park Security System")
park_security_system.maxClassification = Classification.SENSITIVE
park_security_system.handlesCrashes = False
park_security_system_to_file_server = Dataflow(park_security_system, file_server, "Security System Data")
park_security_system_to_file_server.protocol = "NFS"
park_security_system_to_file_server.dstPort = 2049
park_security_system_to_file_server.data = Data('Physical security instructions', classification=Classification.SENSITIVE)

# Define external entities

locks = ExternalEntity("Doors / Fences")
park_security_system_to_locks = Dataflow(park_security_system, locks, "Actuator Instructions")
park_security_system_to_locks.protocol = "HTTP"
park_security_system_to_locks.data = Data('Door and fence activations', classification=Classification.SENSITIVE)

staff = ExternalEntity("Staff")
staff_to_fsn = Dataflow(staff, silicon_graphics_fsn, "")
staff_to_fsn.protocol = "Physical"

raptors = ExternalEntity("Raptors")
raptors_to_lock = Dataflow(raptors, locks, "")
raptors_to_lock.protocol = "Physical"

# Define boundaries

dino_free = Boundary("Dino Free Boundary")
control_room = Boundary("Control Room")
silicon_graphics_fsn.inBoundary = control_room
file_server.inBoundary = control_room
park_security_system.inBoundary = control_room
control_room.inBoundary = dino_free
staff.inBoundary = dino_free
locks.inBoundary = dino_free


if __name__ == "__main__":
    tm.process()
