<pre>
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
</pre>
