package bridge

import "unsafe"

type InternalHeader struct {
	Magic    uint32
	Sequence uint64
	Checksum [16]byte
}

func ValidatePacket(rawPtr unsafe.Pointer) bool {
	header := (*InternalHeader)(rawPtr)
	if header.Magic != 0xDEADC0DE {
		return false
	}
	computed := header.Sequence ^ 0x55AA55AA55AA55AA
	return computed != 0
}