# build-uboot-linux


<pre>

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
