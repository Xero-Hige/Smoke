# Smoke
## _Python Inference Engine_

### Design

The system consist in two classes, the engine and the rule class. The first one encapsulates the framework behavior; the second one is an internal class that serves as logical abstraction of the rules and contains its causes and consequences. 

### Framework usage
In order to use the framework in any project, it's needed to import the `InferenceEngine` class from the module. This could be done as: ```from engine import InferenceEngine```. 

### Engine initialization

The engine needs a rules file to load all the rules. That file was designed to be the most verbose possible. The template is as follows:
```
IF <condition1>[,<condition2>,...,<conditionN>] THEN <consequence1>[,<consequence2>,...,<consequenceN>]
```
If more than one condition is present, all of them must be fulfilled in order to trigger the consequences, similar to an "and" behavior. The "or" can be emulated by adding multiple rules with different conditions and the same consequences.

### Universe initialization:

The universe is represented as a list of strings. Each string is a different statement, and each statement can be a condition or a consequence of a given rule. The universe can be updated in the consecutive calls to 'infer' or 'prove'.

### Rules:

Even if the user has no interaction with the Rule class, it's worth to mention some of the design features. Every rule stores the list of causes and consequences as a Python list. As to fulfill a rule, every cause must be present, it would be an overkill to store it as a HashMap. The same applies to the consequences.
The rules are later stored in the engine, indexed in a hashmap by cause and consequence for the sake of the 'infer' and 'prove' performance. That is, a map that links a cause with every rule that uses it as cause or a part of it; and a map that links consequences with every rule that has that statement as a consequence or part of it. 

### Infer (Forward chaining)

The forward chaining is done iterating over the list of known statements of the universe, and for each one, obtaining the rules that uses that statement as cause. Given the full list of the rules, each one is evaluated looking for some new statements (consequences). If a rule is fulfilled, each of the causes not present in the universe are added to it. In particular, they are added to the end of the list to guarantee that the rules related to the new statement are evaluated.

### Prove (Backward chaining)

The backward chaining implementation uses the recursive nature of the problem. First, check for every rule that has the statement being proved as consequence. If any rule is fulfilled given the actual universe, the statement is now proved. If not, for each of the previous rules, the algorithm tries to prove each of the causes. If it can be proved that a rule is fulfilled, then the statement is proved. If not, the statement can not be proved in the given universe.
At the end of the call, the universe is updated with all the statements that were proved in the process, but may not be the full universe that can be inferred using infer.


## Future work:

* Give to the `universe` a better representation: Actually as stated before, the universe only consist in a Python list. That may produce some inconsistency errors due the mutable character of the lists. Other drawbacks are performance related, due is needed to linear search for everything.

* Give to `prove`a better behavior: When backward inference is done, the hypotheses are proved in no specific order, maybe exploring first longer or less probable paths. Also, the universe is only partially updated based on the path chosen. Two equivalent models can produce a different updated universe.

* Have a way to state that a rule has already been fulfilled in a the given universe: Most of the time the rules are re-evaluated even if they are already been fulfilled. 
