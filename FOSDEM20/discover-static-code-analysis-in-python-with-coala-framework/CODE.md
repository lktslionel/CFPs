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

<br>

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

### Actions

Ypou can specify the actin you want coala to take on a Bear execution.

```ini
[python.autopep8]
bears = ...
default_actions = PEP8Bear: ApplyPatchAction 

# or 
default_actions = *: ApplyPatchAction 

```



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

<br>

### Writing Coala Rules

#### Types

* String (str)
* Float (float)
* Int (int)
* Boolean : true, yes, yeah, no, nope, false
* List of strings (list, values will be split by comma)
* Dict of strings (dict, values will be split by comma and colon)


#### Results


You can retrieve dependency results like this : 

```python
from coalib.bears.LocalBear import LocalBear
from bears.somePathTo.OtherBear import OtherBear

class DependentBear(LocalBear):
    BEAR_DEPS = {OtherBear}

    def run(self, filename, file, dependency_results):
        results = dependency_results[OtherBear.name]
```

`dependency_results` looks like : 

```python
dependency_results = { '<BEAR_NAME>': [...<RESULTS>] }
```

You can use hidden result to share data between Bears.

```python
from coalib.results.HiddenResult import HiddenResult

class OtherBear(LocalBear):

    def run(self, filename, file):
        yield HiddenResult(self, ["Some Content", "Some Other Content"])
```



Default values of `CAN_DECT` and `can fixt`  





#### Dependencies 

You can use `BEAR_DEPS` to list all dependency of your bears.
When they resolved, you get the result through a call to `dependency_results()`.


```python
class BarBear(DependencyBear):
    BEAR_DEPS = {FooBear}
```

You can modify dependencies at runtime by altering `Bear.BEAR_DEPS` variable.


<br>

### Aspect




<br>

### Next UP 

* Better Analysis with ASTs : Provides Universal AST for all language using ANTLR (https://github.com/antlr/grammars-v4)
  that provides a bunch of language's gammar and the ability to parse it with ANTLR.
  project : coAST (https://github.com/coala/coAST)

* Aspects 
* A package manager : https://gitlab.com/coala/package_manager
* Automated Code Review (gitmate)
* coala-utils


* Other metadata

```python
class SomeBear(Bear):
    AUTHORS = {'Jon Snow'}
    AUTHORS_EMAILS = {'jon_snow@gmail.com'}
    MAINTAINERS = {'Catelyn Stark'}
    MAINTAINERS_EMAILS = {'catelyn_stark@gmail.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/80761'
    SEE_MORE = 'https://www.pylint.org'
```    