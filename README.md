# Project
An interpreter for a small, pascal - like language.

# Meet Starlet

## Licensing
**Starlet** programming language is created by [George Manis](http://www.cs.uoi.gr/~manis/) as part of the undergraduate course «Compilers» in Computer Science Department of **University of Ioannina**.
It's purpose is educational and it's goal will be met when the interpreter is complete.
Following is a discription of **Starlet** as composed and handed to class of 2019 by **George Manis**. I'm translating and posting as part of the project's documentation.

## General Discription
**Starlet** supports functions, recursion and nested function declarations plus, three types of variable passing, by reference, by value or by copy. 
It only allows integer values (-32767 < 32767) while string objects are not permitted.

**Starlet's alphabet** includes:
* upper and lower case latin characters («Α»,…,«Ζ» and «a»,…,«z»),
* digits («0»,…,«9»),
* signs for numerical operations («+», «-», «*», «/»),
* relational operators «<», «>», «=», «<=», «>=», «<>»,
* assignment sign «:=»,
* punctuation signs («;», «,», «:»),
* grouping signs («(»,«)»,«[», «]»),
* comment signifiers («/*»,«*/»,«//»).

**Starlet's keywords:**  
program, endprogram  
declare  
if then else endif  
while endwhile dowhile enddowhile  
loop, endloop, exit  
forcase, endforcase, incase, endincase, when, default, enddefault  
function, endfunction, return, in, inout, inandout  
and, or, not  
input, print  

**Order of operation:**
1. «not»,
2. «*», «/»,
3. «+», «-»,
4. «=», «<», «>», «<>», «<=», «>=»,
5. «and»,
6. «or».

**Variable Passing:**  
1. by value: in,  
2. by reference: inout,  
3. by copy: inandout.  

## Grammar  
* *program* ::= **program** id *block* **endprogram**  
* *block* ::= *declarations* *subprograms* *statements*  
* *declarations* ::= (**declare** *varlist*;)*  
* *varlist* ::= ε | id ( , id )*  
* *subprograms* ::= (*subprogram*)*  
* *subprogram* ::= **function** id *funcbody* **endfunction**  
* *funcbody* ::= *formalpars* *block*  
* *formalpars* ::= **(** *formalparlist* **)**  
* *formalparlist* ::= *formalparitem* ( , *formalparitem* )* | ε  
* *formalparitem* ::= **in** id | **inout** id | **inandout** id  
* *statements* ::= *statement* ( ; *statement* )*  
* *statement* ::= ε |  
    *assignment-stat* |  
    *if-stat* |  
    *while-stat* |  
    *do-while-stat* |  
    *loop-stat* |  
    *exit-stat* |  
    *forcase-stat* |  
    *incase-stat* |  
    *return-stat* |  
    *input-stat* |  
    *print-stat*  
* *assignment-stat* ::= id := *expression*  
* *if-stat* ::= **if (** *condition* **)** **then** *statements* *elsepart* **endif**  
* *elsepart* ::= ε | **else** *statements*  
* *while-stat* ::= **while (** *condition* **)** *statements* **endwhile**  
* *do-while-stat* ::= **dowhile** *statements* **enddowhile** **(** *condition* **)**  
* *loop-stat* ::= **loop** *statements* **endloop**  
* *exit-stat* ::= **exit**  
* *forcase-stat* ::= **forcase**  
    ( **when** **(** *condition* **)** : *statements* )**  
    **default:** *statements* **enddefault**  
**endforcase**  
* *incase-stat* ::= **incase**  
    ( **when** **(** *condition* **)** : *statements* )*  
*endincase*  
* *return-stat* ::= **return** *expression*  
* *print-stat* ::= **print** *expression*  
* *input-stat* ::= **input** id*  
* *actualpars* ::= **(** *actualparlist* **)**  
* *actualparlist* ::= *actualparitem* ( , *actualparitem* )* | ε  
* *actualparitem* ::= **in** *expression* | **inout** id | **inandout id**  
* *condition* ::= *boolterm* (**or** *boolterm*)*  
* *boolterm* ::= *boolfactor* (**and** *boolfactor*)*  
* *boolfactor* ::=**not [** *condition* **]** | **[** *condition* **]** | *expression* *relational-oper* *expression*  
* *expression* ::= *optional-sign* *term* ( *add-oper* *term*)*  
* *term* ::= *factor* (*mul-oper* *factor*)*  
* *factor* ::= constant | **(** *expression* **)** | id *idtail*  
* *idtail* ::= ε | *actualpars*  
* *relational-oper* ::= **=** | **<=** | **>=** | **>** | **<** | **<>**  
* *add-oper* ::= **+** | **-**  
* *mul-oper* ::= * | **/**  
* *optional-sign* ::= ε | *add-oper*  


# The Interpreter

### Our interpreter will be completed in 4 phases

### Phase 1 - Lexical and syntax analysis

### Phase 2 - Intermediate code generation

### Phase 3 - Semantic analysis and symbol table

### Phase 4 - Code generation
