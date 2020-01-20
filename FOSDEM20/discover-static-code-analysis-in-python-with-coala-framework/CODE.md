# Code 

> In practice, Coala can detect/fix ..\<STH>
>


<br>  

1. List all available bears : 

    ```
    coala --show-bears
    ```

2. Use one or more Bears
    ```
    coala --files=src/\*.c --bears=SpaceConsistencyBear[,<BEAR>...] 
    ```

    Use `--save` to save params to our .coalafile. It looks like : 
    
    ```ini
    [cli]
    bears = SpaceConsistencyBear
    files = src/*.c
    use_spaces = True
    
    ; If you want to allways save
    save = True  
    ```

    > Use `.coalafile` to set params if you want to go with the  `--non-interactive` mode

3. Learn more about the `.coalafile`
   
   * `[cli]` section is he default section of the file. 
   * To specify sections on CLI, use the `-S` option : 

     ```
     coala -S <SECTION>.<SETTING_KEY>=<SETTING_VALUE>

     # Eg: 
     $: coala -S Makefiles.bears=LineLengthBear

     # [Makefiles]
     # bears = LineLengthBear
     # files = Makefile
     ```

4. Auto-Applying patches 

    * CLI

    ```
    coala ... --apply-patches
    ```

    * use Config `default_actions=...` 