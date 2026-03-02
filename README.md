# build-uboot-linux


<pre>



sudo apt-get install gcc-aarch64-linux-gnu
sudo apt-get install libgnutls28-dev bc bison flex libssl-dev make

# 1. 徹底清除之前的編譯快取
make distclean

# 2. 設定樹莓派 4 的預設配置 (64位元)
make  CROSS_COMPILE=aarch64-linux-gnu- rpi_4_defconfig

# 3. 正式編譯
make  CROSS_COMPILE=aarch64-linux-gnu- -j$(nproc)

config.txt
    ------->
        arm_64bit=1
        enable_uart=1
        kernel=u-boot.bin

編譯成功後，最重要的檔案通常就在根目錄下：

    u-boot.bin：這是最原始的二進位檔案，也是樹莓派 4 最常使用的檔案。
    u-boot：這是包含符號表的 ELF 格式檔案，可用於除錯。
    u-boot.cfg：目前的編譯配置摘要。

3. 其他重要組件
根據您的編譯配置，可能還會看到：

    arch/arm/dts/*.dtb：編譯出的設備樹檔案（Device Tree Blobs）。
    tools/mkimage：這是一個非常有用的工具，後續若要製作自定義引導鏡像會用到。

sudo apt-get install qemu-system-arm

    qemu-system-aarch64 \
    -M raspi4b \
    -display none \
    -serial stdio \
    -kernel u-boot.bin \
    -dtb arch/arm/dts/bcm2711-rpi-4-b.dtb

    | grep -i "RASPI"

qemu-system-aarch64 -M help



    
2. mkimage 具體做了什麼？
當你使用 mkimage 時，它會在原始文件（如 zImage）前面加上一個 64 字節的 Header（信頭）： 

    記錄身份：標註這是 Linux 內核、ARM 架構、是否壓縮等。
    指定位置：告訴 U-Boot 鏡像應該加載到內存的哪個地址（Load Address）以及從哪裡開始執行（Entry Point）。
    校驗安全：生成 CRC 效驗碼，確保文件在傳輸或燒錄過程中沒有損壞。 

3. 常見的應用場景

    製作 uImage：將 Linux 的 zImage 轉換為 U-Boot 專用的 uImage。
    製作 FIT Image：現代化的打包方式，將內核、設備樹、多個配置全部打包成一個文件（.itb），並支持簽名加密以實現安全啟動 (Secure Boot)。 




    重新編譯 U-Boot（針對 virt 平台）：
bash

make distclean
make CROSS_COMPILE=aarch64-linux-gnu- qemu_arm64_defconfig
make CROSS_COMPILE=aarch64-linux-gnu- -j$(nproc)

Use code with caution.
執行模擬：
bash

qemu-system-aarch64 \
    -M virt \
    -cpu cortex-a72 \
    -display none \
    -serial stdio \
    -bios u-boot.bin



    查看硬體資訊 (最基本的儀式感)
這可以讓你看到 U-Boot 辨識出的虛擬硬體參數。

    bdinfo：查看板卡資訊（記憶體位址、乙太網路 MAC 等）。
    printenv：列出所有環境變數。這是 U-Boot 的靈魂，決定了它如何啟動系統。
    version：查看編譯版本與工具鏈資訊。

2. 玩轉記憶體 (底層工程師必備)
你可以直接讀寫 RAM 位址，這在除錯時非常有用。

    md 0x40000000 0x10：讀取（Memory Display）特定位址的內容。
    mw 0x40000000 0x12345678：寫入（Memory Write）一個數值到記憶體。
    nm 0x40000000：進入互動模式修改記憶體內容（輸入新值後按 Enter）。

3. 測試虛擬網路 (如果 QEMU 有設定)
試試看能不能與外界通訊：

    ping 192.168.1.1：(需配合 QEMU 網路參數設定) 測試網路協議棧是否正常運作。

4. 練習修改啟動流程 (最實用的技能)
你可以修改 bootdelay（倒數時間）或自定義指令：

    setenv bootdelay 10：把啟動倒數改長一點。
    setenv my_hello "echo Hello World from U-Boot!"：自定義變數。
    run my_hello：執行自定義指令。
    saveenv：將修改永久存檔（但在 QEMU 沒掛載虛擬 Flash 的情況下可能會失敗）。



 U-Boot 命令需要手動輸入或寫死在源代碼中，非常不靈活。有了 boot.scr，你只需要修改這個文件，就能改變啟動行為（例如切換不同的操作系統或開啟偵錯模式），而不需要重新編譯整個 U-Boot。

與 mkimage 的關係
這就是為什麼你之前會看到 mkimage 這個工具。

    原始文件：通常叫 boot.cmd，是一個純文字檔，裡面寫滿了 U-Boot 命令（如 fatload、setenv、bootz）。
    轉換過程：U-Boot 為了安全和識別，不能直接讀取純文字。你需要用 mkimage 工具給它加上一個 64 字節的 Header（信頭）。
    生成結果：轉換後的二進位文件就是 boot.scr

常見的製作流程

    編寫 boot.cmd（內容範例）：
    bash

    fatload mmc 0:1 0x80800000 zImage
    fatload mmc 0:1 0x83000000 sun8i-v3s-sidewinder.dtb
    setenv bootargs console=ttyS0,115200 root=/dev/mmcblk0p2 rootwait panic=10
    bootz 0x80800000 - 0x83000000

    Use code with caution.
    使用 mkimage 封裝：
    bash

    mkimage -C none -A arm -T script -d boot.cmd boot.scr

    Use code with caution.
     

4. 總結其作用

    自動化：開機後自動執行一連串指令，無需人工干預。
    靈活性：支援 A/B 分區切換、多重引導（Multi-boot）等複雜邏輯。
    通用性：讓同一個 U-Boot 鏡像能透過不同的 boot.scr 啟動不同的 Linux 發行版。


















    

    
apt list --manual-installed
在现代开发中，
    sudo apt install global       ---------------->        gtags -v    ---->  F1 -----> Global: Rebuild Gtags Database
LSP (Language Server Protocol) 确实已经取代了传统标签系统（Tags），成为了绝大多数开发者的“主流”选择
-----------------------------------------------------------------------------------------------------------
</pre>


<pre>

Bionic vs. glibc: Android 甚至連你提到的 glibc 都換掉了，改用 Google 自己寫的 Bionic C Library。

syscall 


</pre>

<pre>


硬體 (Hardware)
核心 (Kernel)：Linux Kernel
初始化系統 (Init System)：systemd (PID 1)
系統服務：網路、日誌 (journald)、硬體管理
桌面環境 / 外殼 (Shell)：圖形介面或終端機










    / (Root): 根目錄。所有目錄和檔案的起點，就像樹的樹幹。
    /bin (Binaries): 基本執行檔。存放系統啟動時或一般使用者都會用到的基本指令，例如 ls, cp, cat。
    /etc (Editable Text Configurations): 系統設定檔。

        這是最重要的目錄之一。幾乎所有系統層級的軟體設定都放在這裡。例如網路設定、使用者密碼檔 (/etc/passwd)、開機啟動流程等。

    /var (Variable Files): 變動資料。

        專門存放「經常變動」的檔案。最常見的是 Log 紀錄檔 (在 /var/log 下)、郵件佇列、快取 (Cache) 或資料庫檔案。

    /home: 使用者家目錄。存放一般使用者的個人資料與個人設定。例如使用者 kevin 的檔案會放在 /home/kevin。
    /root: 系統管理員 (Superuser) 的家目錄。為了安全起見，root 的家目錄與一般使用者分開。

進階與系統相關目錄

    /usr (User System Resources): 第二層應用程式。

        這不是存放「使用者個人資料」，而是存放系統安裝的軟體（如編譯器、函式庫）。你可以把它想像成 Windows 的 C:\Program Files。

    /dev (Devices): 裝置檔案。Unix 秉持「一切皆檔案」的哲學，硬體裝置（如硬碟、滑鼠）在這裡都以檔案形式呈現。
    /proc: 虛擬檔案系統。它不佔用硬碟空間，而是存在記憶體中，用來觀察目前的行程 (Process) 狀態和系統資訊。
    /tmp (Temporary): 暫存檔。存放程式執行時產生的臨時資料，系統通常會在重新開機時清空。 

    /etc	設定檔目錄	系統與服務的設定 (Config files)
/var/log	日誌檔 / Log 檔	記錄系統運行狀況、錯誤訊息
/bin & /sbin	執行檔目錄	系統指令 (sbin 多為管理員指令)
/lib	函式庫	程式運行所需的 Library
/mnt & /media	掛載點	外部硬碟、USB 隨身碟掛載的位置


4. 模組化核心設計 (LKM)
雖然 Linux 是「單核心 (Monolithic Kernel)」，但它引入了 可載入核心模組 (Loadable Kernel Modules) 技術

Linus Torvalds 

(procfs)  只要用 cat 或 grep 就能除錯

Virtual File System, VFS   VFS 定義了一套標準的「檔案操作行為」（如 open, read, write）。
會向 procfs 註冊一個「處理函式」。

公平與效率： 從早期的簡單排程，到後來的 CFS (完全公平排程器)，Linux 核心不斷進化，確保伺服器在跑幾千個任務時也不會卡死。

 Binary Debugger 
Linux 的效能監控工具（如 Prometheus 或 Grafana）

 
 賦能給第三方工具： 因為有了 /proc，全世界的開發者只要寫幾行程式去「讀檔案」，就能開發出各式各樣的工具。例如：

    free 指令：其實只是去讀 /proc/meminfo 然後排版。
    top 指令：其實是去掃描 /proc/[PID]/stat 裡面的數據。


總結
systemd 並不是「變」出資料，它只是：

    利用 Linus 核心 準備好的 cgroups 數據。
    透過 glibc 提供的標準檔案操作函數（如 open, read）。
    定期去查看這些位於 /proc 或 /sys 下的數值。

所以，systemd 其實是一個「高級的檔案閱讀器 + 決策者」。

</pre>

<pre>
技術會過時，但接口（Interface）和標準（Standard）才是永恆的。

核心庫：Linux 用的是 libc.so.6；Windows 則是用 msvcrt.dll 或現代化的 通用 C 執行庫 (Universal CRT / UCRT) (ucrtbase.dll)。

在 Windows，你的程式甚至不能直接跟 Kernel 對話。你必須先跟 kernel32.dll 或 ntdll.dll 溝通，它們再幫你轉達給 Windows 的內核執行層。

Ubuntu 使用 GNU C Library (glibc)，功能全但體積巨大；OpenWrt 則使用 musl libc，體積極小 
Ubuntu 使用 systemd，它非常強大但極其複雜且佔資源。
OpenWrt 自研了 procd。它是為了「路由器場景」量身定做的：它知道什麼時候該重啟網絡，如何處理 Hotplug 事件，且佔用內存微乎其微。        

4. 真正需要動內核的人
只有在以下情況，你才需要去啃那堆「只有作者才懂」的代碼：

    新芯片適配：你要把 OpenWrt 刷入一個市面上還沒支持的路由器。
    寫驅動：你接了一個特殊的感測器，內核裡沒有現成的驅動。
    性能極限優化：比如像 eBPF 這種新技術，需要深入內核來做極速的數據包轉發。

3. 對比表：App 如何利用 Kernel
特性	Ubuntu (通用 Linux)	OpenWrt (嵌入式)
配置管理	各自為政 (JSON, YAML, XML, Conf)	UCI (統一配置文件格式)
進程通信	DBus, Sockets, Pipes	ubus (輕量級 JSON 總線)
網絡管理	NetworkManager / Netplan	netifd (專門針對路由器的網絡守護進程)
初始化系統	systemd (功能強大但臃腫)	procd (極簡，深度集成內核監控)

</pre>

<pre>
winget install GitHub.cli
gh auth login
gh workflow list
gh workflow run <workflow_file.yml>
gh run list
gh run view <run-id> --logs


fork
自己改 driver
改 memory layout
改 board init
改 device tree
加 debug log
改 relocation
CI 才真正有意義。
</pre>

<pre>

          name: qemu-images
          path: |
            u-boot-bin
            zImage
            vexpress.dtb

1. 暫存更改 (Stage Changes) 
在 VS Code 左側活動欄點擊 原始碼控制 圖標（圖標看起來像一個分支節點，快捷鍵 Ctrl+Shift+G）。 
Graphite
Graphite
 +1
你會在「變更 (Changes)」清單下看到你修改過的文件。
點擊文件旁邊的 「+」號，將其移動到「暫存的變更 (Staged Changes)」中。如果你想一次暫存所有文件，點擊「變更」右側的 「+」號。 
Visual Studio Code
Visual Studio Code
 +2
2. 提交代碼 (Commit) 
在頂部的文本框中輸入你的 提交訊息（例如：「feat: 完成登錄功能」或「fix: 修復樣式問題」）。
點擊文本框上方的 「提交 (Commit)」 按鈕，或者按下 Ctrl+Enter。此時代碼已儲存在本地倉庫。 
Visual Studio Code
Visual Studio Code
 +2
3. 推送到遠端 (Push)
提交完成後，點擊藍色的 「同步變更 (Sync Changes)」 按鈕，這會同時執行 Pull 和 Push，將本地代碼上傳到雲端（如 GitHub）。
或者點擊「原始碼控制」標題欄右側的 「...」 三個點圖標，選擇 「推送 (Push)」。 
Visual Studio Code
Visual Studio Code
 +3
提示：
藍線/綠線： 編輯器行號旁的藍線表示修改，綠線表示新增，紅箭頭表示刪除。
文件標記： 文件名旁的 M 代表已修改 (Modified)，U 代表未追蹤 (Untracked，通常是新文件)。 
YouTube
YouTube
 +1
</pre>



</pre>

第一階段：編譯期（找字典）
當你執行 gcc hello.c -o hello 時，發生了以下關鍵步驟：

    標頭檔路徑： 編譯器看到 #include <stdio.h>，它會去 /usr/include/ 找這個檔案。這就是 glibc 提供的「合約」，告訴編譯器 printf 函數長什麼樣子。
    符號解析： 編譯器發現你用了 printf，但它不知道 printf 的實作碼在哪。它會留下一個「標籤」，標註這需要連結到 libc.so.6。
    動態連結： 編譯完成的二進位檔 hello 裡會記錄：「執行我時，請幫我載入 libc.so.6」。

第二階段：執行期（跨越國境）
當你在 Shell 輸入 ./hello 並按下 Enter 時，真正的魔術發生了：

    載入器 (Loader)：
    Linux 核心（Linus 的部分）接收到執行請求，會先啟動一個「動態連結器」（通常是 /lib64/ld-linux-x86-64.so.2）。這個連結器會把 libc.so.6（glibc 的實體）載入到記憶體中。
    跳轉到 glibc：
    你的程式執行 printf。這時程式碼會跳轉到記憶體中 glibc 實作 printf 的位置。
    glibc 的封裝：
    printf 是一個很複雜的函數（要處理格式化、緩衝區等）。但在最底層，它必須把字串「印到螢幕」。這時，glibc 會準備好「系統呼叫 (System Call)」。

第三階段：最關鍵的「交棒」 (System Call)
這是 glibc 與 Linux 核心 最重要的對話點：

    準備暫存器： glibc 會把 write 這個系統呼叫的編號（例如在 x86_64 上是 1）放到 CPU 的暫存器中，並把字串的記憶體位址也放進去。
    觸發指令： glibc 執行一條特殊的 CPU 指令（通常是 syscall）。
    切換模式：
        這條指令會讓 CPU 從 「使用者模式 (User Mode)」 切換到 「核心模式 (Kernel Mode)」。
        這時，控制權正式從 glibc 移交給了 Linus 寫的 Linux 核心。
    核心執行： 核心（Linus 的代碼）看到編號是 1，知道你要寫入資料，於是它去驅動顯示卡或終端機，把 "Hello Linux" 印出來。

</pre>

<pre>

在 systemd 出現之前，如果 A 服務依賴 B 服務，A 必須等 B 完全啟動（Listen 成功）才能開始。systemd 創始人 Lennart Poettering 借鑒了 Apple Launchd 的靈感，開發了以下三種核心機制來達成「並行啟動」：
1. Socket 啟動 (Socket Activation) —— 最天才的騙術
這是 systemd 實現並行的核心。

    傳統做法： 核心啟動 B
    B 建立 Socket
    B 開始監聽
    核心啟動 A
    A 連接 B。
    systemd 做法： systemd 一開機就幫所有服務把 Socket 全部先建立好（但不啟動服務內容）。
    並行原理： systemd 同時啟動 A 和 B。如果 A 速度快，發送請求給 B，這個請求會先卡在核心的 Buffer (緩衝區) 裡。A 不會報錯，只會在那等。等到 B 啟動完成，它直接接手那個已經存在的 Socket，讀取 Buffer 裡的資料並處理。
    結論： A 和 B 在核心看來是同時執行的，相依性被「緩衝化」了。

2. D-Bus 匯流排啟動 (D-Bus Activation)
在 Linux 桌面環境（如 GNOME）中，服務之間透過 D-Bus 通訊。

    systemd 會先攔截所有的 D-Bus 請求。
    當 A 尋找 B 的服務路徑時，systemd 會告訴 A：「找到了，請發送訊息」。
    如果 B 還沒開好，systemd 會排隊（Queue）這些訊息，直到 B 準備好。

3. 自動掛載 (Autofs) 邏輯
對於檔案系統的相依性：

    如果 A 需要掛載 /var/log，systemd 會建立一個虛擬的掛載點（Automount point）。
    A 可以立刻啟動並嘗試寫入檔案。
    直到 A 真正發出「寫入」指令的那一刻，I/O 會暫時阻塞（Blocking），systemd 在背景火速掛載好硬碟，然後放行寫入。

為什麼這不是「協程」？

    協程通常是在「單一執行緒」內切換上下文，避免等待 I/O。
    systemd 利用的是 核心緩衝區 (Kernel Buffering) 與 並行行程 (Parallel Processes)。

</pre>


<pre>

如果把一個運作中的 Linux 系統比喻成一個生態系：

    Linux 核心 (Linus 寫的)： 是地板、空氣和水（基礎資源管理）。
    glibc (GNU 提供的)： 是通用的語言（讓大家能溝通）。
    個人程序 / 服務： 是住在裡面的居民。
    systemd: 就是這個生態系的總管（Manager）。

systemd 具體在「管理」什麼？
它把你的 個人程序 與 glibc 結合後的產物，包裝成一個個 Unit (單元)。它管理的重點在於：

    生命週期管理：
    它決定你的程式什麼時候開機啟動（ExecStart）、掛掉要不要自動重啟（Restart=always）。
    環境清理：
    你的程式透過 glibc 申請了記憶體、打開了 Socket。當程式當機時，systemd 會利用 Control Groups (cgroups) 確保核心把該程式留下的垃圾（殘留行程、記憶體）全部掃乾淨，不影響別人。
    權限與沙盒：
    它可以在不改動你 C 語言代碼的情況下，限制你的程式只能用多少 CPU、能不能看 /home 目錄。這是在 glibc 之上又加了一層安全防護。

為什麼要「融合」管理？
以前的 Linux（SysV init）管理很鬆散。如果你的程式當機後留下了一個「殭屍行程 (Zombie Process)」，舊系統很難抓到它。
systemd 的做法是：
它把「核心的 cgroup 技術」與「服務啟動腳本」融合。不管你的程式呼叫了多少 glibc 函數、開了多少子行程，只要它們屬於同一個 Service Unit，systemd 就像牽著一條隱形的繩子，隨時可以一網打盡或監控狀態。
總結
你寫的 C 程式 是內容，glibc 是支撐它的骨架，而 systemd 是讓這具骨架能在正確的時間起床、工作、並在生病時自動急救的外骨骼管理系統。
所以，在現代 Linux 開發中，寫好程式只是第一步，寫好一個 .service 設定檔 讓 systemd 來管理它，才是真正讓程式「工業化」運作的關鍵。

</pre>

<pre>
    Ring 0 (核心模式 / Kernel Mode)： 這是最高權限。只有 Linus 寫的核心 跑在這裡。它可以直接下指令給 CPU、記憶體、硬碟，沒有任何限制。
    Ring 3 (使用者模式 / User Mode)： 這是最低權限。你的 個人程序 和 glibc 都跑在這裡。如果你在這裡嘗試直接執行「關閉中斷」或「讀取別人的記憶體」等危險指令，CPU 硬體會直接噴出一個 General Protection Fault（一般保護錯誤）並把你的程式殺掉。

2. glibc 的「翻譯」其實是在「請求過關」
因為你的程式被關在 Ring 3 這個籠子裡，無法直接碰硬體，所以：

    你的程式（Ring 3）求助 glibc。
    glibc 幫你把公文備好，放在 CPU 的「托盤」（暫存器）上。
    執行 syscall：這條指令就像是一個「傳送門」，它會觸發硬體切換 CPU 的特權等級，從 Ring 3 躍升到 Ring 0。
    這時，控制權就交給了守在 Ring 0 入口處的 Linux 核心。

3. 利用核心模式進行「計算」的真相
其實，大部分的「純數學計算」（例如 1+1）都在 Ring 3 就能完成，不需要驚動核心。
真正需要切換到 核心模式 (Ring 0) 的「計算」，通常涉及：

    資源分配： 「給我更多記憶體！」（涉及 頁表管理）。
    硬體通訊： 「把這段文字傳到網路卡！」（涉及 I/O 埠操作）。
    時間與排程： 「我累了，讓別的程式跑一下！」（涉及 Context Switch 上下文切換）。
</pre>



<pre>

RAX3000M 使用的是 聯發科（MediaTek）MT7981B    aarch64-linux-gnu-gcc

增加快取大小：避免大檔案導致傳輸中斷。
git config --global http.postBuffer 524288000 (設為 500MB)
git config --global http.postBuffer 524288000
開啟並行優化：針對檔案數量極多的專案。
git config --global feature.manyFiles true
  
1. 【推薦】使用 QEMU 虛擬平台來測試你的固件功能
如果你主要是想測試 .config 編譯出來的軟體、套件或腳本是否正常運作，建議不要執著於模擬「RAX3000M」這個硬體。
做法： 在 make menuconfig 時，將 Target System 改選為 QEMU ARM Virt。
優點： 這種模式不需要 U-Boot，QEMU 可以直接引導 kernel。你可以把你在 RAX3000M 想要用的套件清單放進去編譯，測試軟體邏輯。
啟動指令範例：
bash
qemu-system-aarch64 -nographic -M virt -cpu cortex-a53 -m 512 \
  -kernel openwrt-armvirt-64-Image-initramfs
</pre>

<pre>
  
  qemu-system-aarch64 \
    -M virt \
    -cpu cortex-a53 \
    -smp 2 \
    -m 512 \
    -kernel <您的內核檔案路徑> \
    -append "root=/dev/vda rootwait console=ttyAMA0" \
    -drive file=<您的emmc鏡像路徑>,format=raw,if=virtio \
    -net nic,model=virtio \
    -net user,hostfwd=tcp::8080-:80 \
    -nographic

    關鍵參數說明：
-M virt: 使用通用虛擬化平台，這是模擬 ARM 路由器的標準做法。
-drive ...,if=virtio: 將您的 eMMC 鏡像模擬為虛擬磁碟。
-net user,hostfwd=tcp::8080-:80: 非常重要！ 這會將虛擬機的 80 埠（LuCI 界面）映射到您電腦的 8080 埠。
-nographic: 讓輸出直接顯示在您的終端機上。

qemu-system-aarch64 -M virt -cpu cortex-a53 -m 512 \
    -drive file=<変換したファイル名>.img,format=raw,if=virtio \
    -net nic -net user \
    -nographic

</pre>

<pre>
  以下是该设备的启动逻辑与结构分析：
1. 启动结构并非完全“固定”
虽然出厂和大多数第三方固件（如 OpenWrt、ImmortalWrt）默认使用 U-Boot，但启动链实际上分为几个阶段，你可以根据需求调整：
ROM Code (BL1): 固化在 MT7981 芯片内部，不可更改。
BL2 (Preloader): 负责初始化 DDR。
BL31 (ATF/TF-A): 负责安全环境和电源管理。
BL33 (U-Boot): 這是你提到的“固定结构”部分。 
OpenWRT
OpenWRT
 +1
2. 为什么通常“一定是” U-Boot？
在 RAX3000M 这种基于 MediaTek Filogic 平台的设备上，U-Boot 被广泛使用是因为：
引导兼容性： 它能正确加载 Linux 内核（uImage/itb 格式）并传递设备树（DTB）。
救砖功能： 第三方“不死 U-Boot”（如 hanwckf 的版本）提供了 Web 刷机界面，即使 Linux 系统崩溃，也能通过 U-Boot 恢复。
分区管理： 它定义了 NAND/eMMC 的分区表结构，决定了内核和 rootfs 存放在哪。 
3. 可选的替代结构
如果你想打破“固定”结构，理论和实践上有以下可能：
直接引导： 一些极简嵌入式系统可以跳过 U-Boot，由 BL2 直接跳转到精简后的内核，但这对 RAX3000M 的复杂驱动初始化非常不利。
UEFI (EDK2): 部分开发者正在为 MT798x 平台适配 UEFI 引导，但这在路由器固件中极少见。
OEM 限制： 移动原厂 U-Boot 带有签名校验，如果你想刷第三方 Linux（OpenWrt），必须更换为支持校验解除的第三方 U-Boot。
</pre>

4. 深度開發：本地 Clone + Quilt 補丁
3. 雲端編譯：GitHub Actions (與 .yml 結合)
2. 修改「特定軟體」：使用 SDK
如果你只想改某一個 App（例如 vlmcsd 或某個驅動）的代碼，而不想編譯整個作業系統
1. 修改「配置」：使用 Image Builder (推薦)
如果你只是想修改預設的網路設定、預裝外掛、或是加入自己的 .sh 腳本，不需要下載完整源碼



1. 核心在於 .config 檔案
在 env 區段可以看到這行：
CONFIG_FILE: .config
這就是 OpenWrt 的「靈魂」。所有的架構選擇（例如是 x86_64、MT7621 還是 ARM）、插件選擇、內核設定，全部都儲存在這個 .config 檔案裡。
流程中發生了什麼：腳本在 Load custom configuration 步驟中，會執行 mv $CONFIG_FILE openwrt/.config。
這意味著：你必須在你的 GitHub 倉庫根目錄下放一個已經設定好的 .config 檔案。如果你沒放，編譯器就會使用 Lean LEDE 源碼 的默認設定。
2. diy-part2.sh 的輔助修改
你在腳本中看到的 DIY_P2_SH: diy-part2.sh 經常被用來透過指令直接修改架構或 IP。
許多人會在 diy-part2.sh 裡寫 sed 指令，例如：
sed -i 's/192.168.1.1/192.168.10.1/g' package/base-files/files/bin/config_generate
甚至可以用指令強制寫入特定的架構參數到 .config 中。
3. make defconfig 自動補全
在 Download package 步驟中，腳本執行了：
make defconfig
這個指令的作用是：檢查當前的 .config 檔案，如果缺少必要的相依性或架構設定，它會根據你提供的基礎設定自動補全剩餘的部分。




<pre>
  我想玩Uboot/ Linux的網絡編程/還有一些零散的内存技術  /還有就是我要用rust寫軟件
這是一個非常紮實的技術路徑。如果你想從 U-Boot（引導加載程序）、Linux 網絡內核 到 Rust 系統編程 全線打通，OpenWrt 確實是最佳的「實驗室」。
以下是你針對這三個方向可以深入研究切入點：
1. U-Boot 與嵌入式底層
U-Boot 是硬體啟動後運行的第一個程式，負責初始化內存並引導內核。
研究重點：
啟動流程：研究 SPL (Secondary Program Loader) 如何將內核從 Flash 搬運到 RAM。
環境變量 (Env)：了解如何通過 U-Boot 命令行修改啟動參數（例如 bootargs）。
救磚機制：學習如何編寫 httpd 或 tftp 模式，在不進入系統的情況下刷機。
實踐建議：去 GitHub - u-boot 查看針對你設備的 board 支持文件，嘗試自己編譯一個能啟動的 u-boot.bin。
2. Linux 網絡編程與內存技術
既然你在用 Lean 的固件，你可以直接觀察那些「激進」的優化是如何操作內核的。
網絡編程 (Kernel Space)：
Netfilter/Iptables：這是 OpenWrt 插件的核心。研究如何寫一個內核模組，攔截或修改經過路由器的封包。
XDP (Express Data Path)：如果你想追求極致性能，這是目前 Linux 網絡編程的最前沿技術，可以在數據包進入協議棧之前就進行處理。
內存技術 (Memory Management)：
DMA (Direct Memory Access)：研究網卡驅動如何不經過 CPU 搬運數據到內存，這在高性能路由器中至關重要。
Zram：OpenWrt 常用的壓縮內存技術，非常適合在內存小的嵌入式設備上練習。
3. 用 Rust 進行開發
Rust 是替代 C 語言進行系統編程的最佳選擇，特別適合編寫高效且安全的路由器插件。
Cross-Compilation (交叉編譯)：
你需要在 PC 上安裝 Rust 並添加目標平台的工具鏈（例如 mips-unknown-linux-musl 或 aarch64-unknown-linux-musl）。
你可以參考 OpenWrt SDK 官方文檔 來編譯你的 Rust 程序。
Rust 插件開發：
代碼實例：可以嘗試用 Rust 寫一個簡單的 DNS 轉發器或流量監控工具。
優勢：Rust 的內存安全特性（Ownership/Borrow Checker）能讓你免於處理嵌入式開發中最頭痛的 Memory Leak 和 Segmentation Fault。
下一步建議
既然你已經會用 SSH 手動配置 .config，你可以：
在 make menuconfig 中勾選 Build the OpenWrt SDK。這會生成一個獨立的開發環境，讓你在不重新編譯整個固件的情況下，快速編譯你寫的 Rust 程式。
搜尋並閱讀 The Rust Embedded Book，這是學習 Rust 進行底層開發的權威指南。
你需要我為你提供一個簡單的 Rust 交叉編譯到 OpenWrt 的 Hello World 流程嗎？



還有什麽好玩的幫我補充一下
既然你已經觸及了 U-Boot、內核網絡 和 Rust，這已經是路由器玩家的「天花板」級別了。要在這個基礎上玩得更深，這裡有幾個非常硬核且有趣的進階方向：
1. 玩轉 eBPF (Extended Berkeley Packet Filter)
這是目前 Linux 內核最火的技術。它允許你在不重新編譯內核的情況下，將自定義的代碼（可以用 Rust 寫）直接注入內核運行。
怎麼玩：在 OpenWrt 上實現一個「零延遲」的防火牆或監控工具。你可以用 Rust 的 Aya 庫 來編寫 eBPF 程序，直接攔截網卡上的原始數據包。
趣味點：這比傳統的 iptables 快得多，是現代高性能網絡開發的必修課。
2. 虛擬化與容器 (LXC/Docker)
如果你編譯的是 X86 或高性能 ARM（如 RK3588），不要只把它當路由器。
怎麼玩：在 OpenWrt 裡跑 LXC (Linux Containers)。你可以同時運行一個 Debian 桌面、一個 Home Assistant 自動化中心和一個 Rust 寫的後台服務，彼此內存隔離但共享內核。
內存技術：研究 KSM (Kernel Same-page Merging)，看看內核如何把多個容器中相同的內存頁合併，以節省路由器的內存。
3. 硬體接口通信 (GPIO / I2C / SPI)
路由器不只有網口。如果你有開發板或帶有擴展引腳的設備，可以玩硬體控制。
怎麼玩：用 Rust 寫一個驅動，通過 GPIO 控制風扇轉速（根據 CPU 溫度），或者外接一個 OLED 小螢幕顯示當前網速和內存佔用。
工具推薦：參考 rust-embedded/embedded-hal 庫。
4. 繞過內核協議棧 (DPDK)
如果你覺得 Linux 內核處理網絡包還是太慢（因為有上下文切換的開銷），你可以嘗試 用戶態網絡。
怎麼玩：研究 DPDK (Data Plane Development Kit)。它直接接管網卡，把數據包直接拉到用戶態（User Space）處理，完全跳過內核。
挑戰：這需要極強的內存管理能力，非常適合練習 Rust 的指針與內存安全特性。
5. 深入研究 OpenWrt 的 「Procd」 守護進程
這是 OpenWrt 的 init 系統（類似 PC 上的 systemd）。
怎麼玩：研究如何用 Rust 寫一個自啟動服務，並與 ubus（OpenWrt 的內部總線）通信。你可以開發一個能被官方 LuCI 界面調用的 Rust 後端，實現前後端完全分離。
6. 自製 U-Boot 啟動動畫或「救磚」網頁
怎麼玩：修改 U-Boot 源碼，在啟動時通過 GPIO 點亮特定編碼的 LED 燈，或者在 U-Boot 階段就實現一個簡易的 Web 服務器用於上傳固件。
總結建議：
你可以先從 「用 Rust 寫一個基於 ubus 的系統監控插件」 開始。這會讓你同時接觸到：
OpenWrt 的進程間通信 (ubus)
Rust 的交叉編譯
Linux 的 /proc 虛擬文件系統（內存與 CPU 數據來源）
你手上現在有哪款具體的硬體設備？（這決定了你是玩 eBPF 還是玩 GPIO 擴展）。




  內存部分：讀取 /proc/meminfo 並解析。
網絡部分：使用 pnet 庫抓取網卡上的原始數據包（Raw Sockets），統計每個 IP 的流量。
挑戰：嘗試將這個程序交叉編譯為你 LEDE 固件對應的架構（如 MIPS 或 ARM）。
</pre>
