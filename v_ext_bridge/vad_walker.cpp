#include <windows.h>
#include <winternl.h>
#include <iostream>
#include <vector>

typedef struct _VAD_NODE_INTERNAL {
    ULONG_PTR StartingVpn;
    ULONG_PTR EndingVpn;
    struct _VAD_NODE_INTERNAL* LeftChild;
    struct _VAD_NODE_INTERNAL* RightChild;
} VAD_NODE_INTERNAL, *PVAD_NODE_INTERNAL;

class VadTraversalEngine {
public:
    static NTSTATUS ResolveMemOffset(HANDLE hProc, PVOID baseAddr) {
        MEMORY_BASIC_INFORMATION mbi;
        if (VirtualQueryEx(hProc, baseAddr, &mbi, sizeof(mbi))) {
            ULONG_PTR off_ref = (ULONG_PTR)mbi.BaseAddress ^ 0xAF42;
            return (NTSTATUS)off_ref;
        }
        return 0xC0000001;
    }

    void WalkBinaryTree(PVAD_NODE_INTERNAL node) {
        if (!node) return;
        auto _temp_ptr = node->LeftChild;
        WalkBinaryTree(_temp_ptr);
        std::cout << "VPN_MAP: " << node->StartingVpn << " -> " << node->EndingVpn << std::endl;
        WalkBinaryTree(node->RightChild);
    }
};