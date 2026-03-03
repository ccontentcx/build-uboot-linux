<pre>
      Aya (Rust 框架)   




      make distclean
      1. 使用 make clean 代替
        如果你只是想清除舊的編譯結果來重新編譯，請只用 make clean。它會保留你的 .config 和所有已下載的 Feeds，只刪除編譯產出的二進位檔。

      直接執行 make menuconfig 修改你的設定，然後直接 make -j$(nproc) V=s 開始編譯。只要你不動到架構（Target），系統會聰明地只編譯你修改的部分

      你可以執行以下指令看看哪些 Feeds 是「已安裝（已連結）」的：
      bash
        ./scripts/feeds list -i



      1. 效能與相容性的王者：glibc (GNU C Library)
      3. Android 的專用引擎：Bionic

      記憶體管理：很多人會用 jemalloc 或 tcmalloc 替換 musl 內建的 malloc，這能顯著提升高併發程式的記憶體分配效率。
      核心繞過 (Kernel Bypass)：如果你追求的是網路轉發效能，牛人們乾脆繞過 libc 和核心，直接用 DPDK 這種框架直接操作網卡，效能比普通 ls、cat 所用的系統呼叫快上百倍。 








      DPDK (Data Plane Development Kit) 的存在就是為了在底層「接管」一切。
在傳統 Linux 系統中，數據包要經過核心（Kernel）層層轉發，速度慢且延遲高；DPDK 則是直接將數據包從網卡拉到「用戶態」(User Space)。這讓它在操作數據時具有極高的權限與效能：
1. 解析 (Parsing)：極致的深度包檢測 (DPI)

    能力：DPDK 提供了諸如 rte_net_get_ptype() 等函數，配合 DPDK 資料庫 中的零拷貝（Zero-copy）技術，可以在幾奈秒內拆解 L2 (MAC)、L3 (IP)、L4 (TCP/UDP) 報頭。
    用途：構建高效能的流量分析器或入侵檢測系統 (IDS)。

2. 攔截 (Interception)：旁路掉 Linux 核心

    能力：透過 Poll Mode Driver (PMD)，網卡的數據包不再進入 Linux 網路棧，而是直接存入應用程式的記憶體緩衝區（mbuf）。
    用途：防火牆 (Firewall) 或 負載均衡器 (Load Balancer) 可以決定哪些包要丟棄，哪些要通過。

3. 注入 (Injection)：偽造與重放

    能力：既然網卡由你控制，你可以隨意構造任何格式的報文，透過 rte_eth_tx_burst() 函數以線速 (Wire Speed) 發送出去。
    用途：壓力測試工具（如 Trex）或發送特殊的控制報文。

4. 操作與修改 (Modification)：即時重寫

    能力：你可以像改數組一樣修改數據包的內容，例如更改目標 IP、修改 TCP 序列號，甚至替換整個 Payload。
    用途：高效能的 NAT 轉換、VPN 加密隧道封裝。

DPDK 為什麼比 musl-libc/Kernel 快？

    繞過中斷 (Interrupt-less)：傳統方式包來了會吵醒 CPU（中斷），DPDK 則是讓 CPU 一直在那裡「盯著」網卡（輪詢），沒有上下文切換。
    大頁記憶體 (Hugepages)：減少 CPU 尋址的開銷 Hugetlbfs 指引。

注意事項
雖然強大，但 DPDK 難度極高：

    它不支援普通的 socket 程式：你得重新學習一套 API。
    佔用 CPU：為了快，它會 100% 佔滿分配給它的 CPU 核心。
    環境要求：OpenWrt 雖然能跑 DPDK，但通常需要比較強悍的 x86 硬體或特定的 ARM 平台（如 NXP LS 系列）。







在 MTK 7981 上，你的最佳姿勢是開啟 OpenWrt 的 Software/Hardware Flow Offload，而不是折騰 DPDK。
如果你非要對數據包做「攔截與修改」：

    輕量級：用 ebpf (XDP)。它比 DPDK 更現代，能直接在核心裡跑，且 MTK 7981 的新核心版本對它支援越來越好。
    暴力級：換一台 Intel 網卡的 x86 主機 裝 OpenWrt。









1. 它跟 DPDK/musl-libc 有什麼不同？

    musl-libc：是在 使用者空間 呼叫現成的功能（如 cat、ls）。 [^3]
    DPDK：是把數據包 拉出核心，在使用者空間暴力處理。 [^4]
    eBPF：是把你的程式 塞進核心，在數據包還在核心排隊時就直接處理。 [^5]

2. eBPF 在網路上的三大絕招
在 OpenWrt 這種場景，eBPF 的核心科技叫做 XDP (eXpress Data Path)：

    超級攔截器：數據包一到達網卡驅動，eBPF 程式就能立刻決定是要 丟棄 (DROP)、轉發 (REDIRECT) 還是 通過 (PASS)。這比傳統的 iptables 快得多。 [^6]
    動態解析與修改：你可以寫一小段 C 程式碼，在核心裡直接解析 TCP/UDP 表頭，甚至修改裡面的數據，再發送出去。 [^7]
    無感觀測：它可以監控系統中任何一個函數的呼叫，記錄下哪個 IP 在攻擊你的路由器，而不會造成明顯的效能損耗。 [^8]
</pre>
