from pythautomata.base_types.state import State
from pythautomata.base_types.symbol import SymbolStr
from pythautomata.base_types.alphabet import Alphabet
from pythautomata.automata.wheighted_automaton_definition.weighted_automaton import WeightedAutomaton
from pythautomata.automata.wheighted_automaton_definition.weighted_state import WeightedState
from pythautomata.model_comparators.hopcroft_karp_comparison_strategy import HopcroftKarpComparisonStrategy as HopcroftKarpComparisonStrategy

binaryAlphabet = Alphabet(frozenset((SymbolStr('0'), SymbolStr('1'))))
zero = binaryAlphabet['0']
one = binaryAlphabet['1']


class WeightedTomitasGrammars:
    """
    Class containing weighted (probabilistic) versions of automata from paper:    
        Tomita, M. (1982). 
        Dynamic Construction of Finite Automata from examples using Hill-climbing. 
        Proceedings of the Fourth Annual Conference of the Cognitive Science Society 
        (p./pp. 105--108), Ann Arbor, Michigan.

    The weighted version is taken from paper:
        Weiss, Gail & Goldberg, Yoav & Yahav, Eran. (2019). 
        Learning Deterministic Weighted Automata with Queries and Counterexamples. 

    Methods
    -------   
    get_all_automata: list(WeightedAutomaton)
        returns a list containing all weigthed automata defined in this class

    get_automaton_1: WeightedAutomaton
        returns the weighted automaton 1 from the paper
    
    get_automaton_2: WeightedAutomaton
        returns the weighted automaton 2 from the paper

    get_automaton_3: WeightedAutomaton
        returns the weighted automaton 3 from the paper

    get_automaton_4: WeightedAutomaton
        returns the weighted automaton 4 from the paper

    get_automaton_5: WeightedAutomaton
        returns the weighted automaton 5 from the paper

    get_automaton_6: WeightedAutomaton
        returns the weighted automaton 6 from the paper

    get_automaton_7: WeightedAutomaton
        returns the weighted automaton 7 from the paper
    """

    @staticmethod
    def get_all_automata():
        """
        Method returning a list of all automata of the class

        Returns
        -------
        list(WeightedAutomaton)
            all automata defined in the class
        """
        return [
            WeightedTomitasGrammars.get_automaton_1(),
            WeightedTomitasGrammars.get_automaton_2(),
            WeightedTomitasGrammars.get_automaton_3(),
            WeightedTomitasGrammars.get_automaton_4(),
            WeightedTomitasGrammars.get_automaton_5(),
            WeightedTomitasGrammars.get_automaton_6(),
            WeightedTomitasGrammars.get_automaton_7()
        ]
        
    @staticmethod
    def get_automaton_1():
        """
        method with specification of automaton 1 from the paper       

        Returns
        -------
        WeightedAutomaton
            weighted tomita grammar 1
        """
        q0 = WeightedState("q0", 1, 0.05)
        q1 = WeightedState("q1", 0, 0.05)

        q0.add_transition(zero, q1, 0.665)
        q0.add_transition(one, q0, 0.285)
        q1.add_transition(zero, q1, 0.285)
        q1.add_transition(one, q1, 0.665)

        states = {q0, q1}
        #comparator = HopcroftKarpComparisonStrategy()
        return WeightedAutomaton(binaryAlphabet, states, SymbolStr("$"), "WeightedTomitas1")

    @staticmethod
    def get_automaton_2():
        """
        method with specification of automaton 2 from the paper       

        Returns
        -------
        WeightedAutomaton
            weighted tomita grammar 2
        """
        q0 = WeightedState("q0", 1, 0.05)
        q1 = WeightedState("q1", 0, 0.05)
        q2 = WeightedState("q2", 0, 0.05)

        q0.add_transition(zero, q2, 0.665)
        q0.add_transition(one, q1, 0.285)
        q1.add_transition(zero, q0, 0.285)
        q1.add_transition(one, q2, 0.665)
        q2.add_transition(zero, q2, 0.285)
        q2.add_transition(one, q2, 0.665)

        states = {q0, q1, q2}
        #comparator = HopcroftKarpComparisonStrategy()
        return WeightedAutomaton(binaryAlphabet, states, SymbolStr("$"), "WeightedTomitas2")

    @staticmethod
    def get_automaton_3():
        """
        method with specification of automaton 3 from the paper       

        Returns
        -------
        WeightedAutomaton
            weighted tomita grammar 3
        """
        q0 = WeightedState("q0", 1, 0.05)
        q1 = WeightedState("q1", 0, 0.05)
        q2 = WeightedState("q2", 0, 0.05)
        q3 = WeightedState("q3", 0, 0.05)
        q4 = WeightedState("q4", 0, 0.05)

        q0.add_transition(zero, q0, 0.665)
        q0.add_transition(one, q1, 0.285)
        q1.add_transition(zero, q2, 0.665)
        q1.add_transition(one, q0, 0.285)
        q2.add_transition(zero, q3, 0.285)
        q2.add_transition(one, q4, 0.665)
        q3.add_transition(zero, q2, 0.665)
        q3.add_transition(one, q3, 0.285)
        q4.add_transition(zero, q4, 0.285)
        q4.add_transition(one, q4, 0.665)

        states = {q0, q1, q2, q3, q4}
        #comparator = HopcroftKarpComparisonStrategy()
        return WeightedAutomaton(binaryAlphabet, states, SymbolStr("$"), "WeightedTomitas3")

    @staticmethod
    def get_automaton_4():
        """
        method with specification of automaton 4 from the paper       

        Returns
        -------
        WeightedAutomaton
            weighted tomita grammar 4
        """
        q0 = WeightedState("q0", 1, 0.05)
        q1 = WeightedState("q1", 0, 0.05)
        q2 = WeightedState("q2", 0, 0.05)
        q3 = WeightedState("q3", 0, 0.05)

        q0.add_transition(zero, q1, 0.665)
        q0.add_transition(one, q0, 0.285)
        q1.add_transition(zero, q2, 0.665)
        q1.add_transition(one, q0, 0.285)
        q2.add_transition(zero, q3, 0.665)
        q2.add_transition(one, q0, 0.285)
        q3.add_transition(zero, q3, 0.285)
        q3.add_transition(one, q3, 0.665)

        states = {q0, q1, q2, q3}
        #comparator = HopcroftKarpComparisonStrategy()
        return WeightedAutomaton(binaryAlphabet, states, SymbolStr("$"), "WeightedTomitas4")

    @staticmethod
    def get_automaton_5():
        """
        method with specification of automaton 5 from the paper       

        Returns
        -------
        WeightedAutomaton
            weighted tomita grammar 5
        """
        q0 = WeightedState("q0", 1, 0.05)
        q1 = WeightedState("q1", 0, 0.05)
        q2 = WeightedState("q2", 0, 0.05)
        q3 = WeightedState("q3", 0, 0.05)

        q0.add_transition(zero, q3, 0.665)
        q0.add_transition(one, q1, 0.285)
        q1.add_transition(zero, q2, 0.285)
        q1.add_transition(one, q0, 0.665)
        q2.add_transition(zero, q1, 0.285)
        q2.add_transition(one, q3, 0.665)
        q3.add_transition(zero, q0, 0.285)
        q3.add_transition(one, q2, 0.665)

        states = {q0, q1, q2, q3}
        #comparator = HopcroftKarpComparisonStrategy()
        return WeightedAutomaton(binaryAlphabet, states, SymbolStr("$"), "WeightedTomitas5")

    @staticmethod
    def get_automaton_6():
        """
        method with specification of automaton 6 from the paper       

        Returns
        -------
        WeightedAutomaton
            weighted tomita grammar 6
        """
        q0 = WeightedState("q0", 1, 0.05)
        q1 = WeightedState("q1", 0, 0.05)
        q2 = WeightedState("q2", 0, 0.05)

        q0.add_transition(zero, q2, 0.665)
        q0.add_transition(one, q1, 0.285)
        q1.add_transition(zero, q0, 0.285)
        q1.add_transition(one, q2, 0.665)
        q2.add_transition(zero, q1, 0.285)
        q2.add_transition(one, q0, 0.665)

        states = {q0, q1, q2}
        #comparator = HopcroftKarpComparisonStrategy()
        return WeightedAutomaton(binaryAlphabet, states, SymbolStr("$"), "WeightedTomitas6")

    @staticmethod
    def get_automaton_7():
        """
        method with specification of automaton 7 from the paper       

        Returns
        -------
        WeightedAutomaton
            weighted tomita grammar 7
        """
        q0 = WeightedState("q0", 1, 0.05)
        q1 = WeightedState("q1", 0, 0.05)
        q2 = WeightedState("q2", 0, 0.05)
        q3 = WeightedState("q3", 0, 0.05)
        q4 = WeightedState("q4", 0, 0.05)

        q0.add_transition(zero, q0, 0.665)
        q0.add_transition(one, q1, 0.285)
        q1.add_transition(zero, q2, 0.665)
        q1.add_transition(one, q1, 0.285)
        q2.add_transition(zero, q2, 0.665)
        q2.add_transition(one, q3, 0.285)
        q3.add_transition(zero, q4, 0.665)
        q3.add_transition(one, q3, 0.285)
        q4.add_transition(zero, q4, 0.285)
        q4.add_transition(one, q4, 0.665)

        states = {q0, q1, q2, q3, q4}
        #comparator = HopcroftKarpComparisonStrategy()
        return WeightedAutomaton(binaryAlphabet, states, SymbolStr("$"), "WeightedTomitas7")