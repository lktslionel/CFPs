# Code 

> In practice, Coala can detect/fix ..\<STH>
>



<br>  
<br>

### Basics 

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


<br>

### Configuration 


#### 3 main scopes 

```
+--------------------------------------------------+
|                                                  |
| SYSTEM         +------------------------------+  |
| system_coafile |                              |  |
|                | User     +----------------+  |  |
|                | .coarc   | PRJ            |  |  |
|                |          | .coafile       |  |  |
|                |          +----------------+  |  |
|                |                              |  |
|                +------------------------------+  |
|                                                  |
+--------------------------------------------------+
```

`->`: Means overrides 

`.coafile -> .coarc -> system_coafile`

### Inheritance in config files 

Use `+=` A build an accumulated list.

```
[all]
enabled = True
overridable = 2
ignore = vendor1/

[all.section1]
overridable = 3
ignore += vendor2/
other = some_value

[all.section2]
overridable = 4
ignore += vendor3/
other = some_other_value
```



<br>

### Quickstart setup 

Simply run `coala-quickstart` in your root directory, to create a new `.coafile` pre-filled with a basic set of configuration entries.

It will also sugget you, some starting bears based on some assumptions.


<br>

### Bears


* Native Bears : Already implemented Bears
* Linter Bears : Wrap your tool 
* External Bears : Not a python programmer; write bears in other languages

Brings your software quality UP !!!!



<br>

### Regex 

You can test your regex or file globbing with the python console : 

```
$ python
> from coalib.parsing.Globbing import fnmatch
```

Ref : https://docs.coala.io/en/latest/Users/Glob_Patterns.html



<br>

### Exit code 


| CODE  | DESC | 
|--|--|
|0 | coala executed successfully but yielded no results.|
|1 | coala executed successfully but yielded results.|
|2 | Invalid arguments were passed to coala in the command line.|
|3 | The file collector exits with this code if an invalid pattern |is passed to it.
|4 | coala was executed with an unsupported version of python|
|5 | coala executed successfully. Results were found but patches to |the results were applied successfully
|13 | There is a conflict in the version of a dependency you have |installed and the requirements of coala.
|130 | A KeyboardInterrupt (Ctrl+C) was pressed during the execution |of coala.
|255 | Any other general errors.|

<br>

### Git hook

It's a great idea too use `coala` on a giit pre-commit hook.

Use this boilerplate script 

```sh
#!/bin/sh
set -e
coala
```

<br>

### CI / CD


To run coaloa as CI script 

```sh
coala --ci 

# or 

coala --non-interactive 
```
