<pre>
      make distclean
      1. 使用 make clean 代替
        如果你只是想清除舊的編譯結果來重新編譯，請只用 make clean。它會保留你的 .config 和所有已下載的 Feeds，只刪除編譯產出的二進位檔。

      直接執行 make menuconfig 修改你的設定，然後直接 make -j$(nproc) V=s 開始編譯。只要你不動到架構（Target），系統會聰明地只編譯你修改的部分

      你可以執行以下指令看看哪些 Feeds 是「已安裝（已連結）」的：
      bash
        ./scripts/feeds list -i
</pre>
