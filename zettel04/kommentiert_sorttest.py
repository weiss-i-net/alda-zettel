import pytest
from random import randint
import collections
from copy import deepcopy
from operator import itemgetter, attrgetter

class Student:
    def __init__(self, name, mark):
        '''Construct new Student object with given 'name' and 'mark'.'''       # comment: Konvention: """ statt ''' für Docstrings
        self.name = name                                                       # comment: Interne Variablen sollten immer mit _ oder __ beginnen,
        self.mark = mark                                                       #          e.g. self._name

    def get_name(self):                                                        # comment: In den Docstrings kann mit :param name: und :return:
        '''Access the name.'''                                                 #          eine Beschreibung der Parameter und der Rückgabewerte
        return self.name                                                       #          eingefügt werden.

    def get_mark(self):
        '''Access the mark.'''
        return self.mark

    def __repr__(self):
        '''Convert Student object to a string.'''
        return "%s: %3.1f" % (self.name, self.mark)

    def __eq__(self, other):
        '''Check if two Student objects are equal.'''
        return self.name == other.name and self.mark == other.mark

##################################################################

def insertion_sort_1(a, key=lambda x: x):
    '''
    Sort the array 'a' in-place.

    Parameter 'key' must hold a function that, given a complicated
    object, extracts the property to sort by. By default, this
    is the object itself (useful to sort integers). To sort Students
    by name, you call:
        insertion_sort_1(students, key=Student.get_name)
    whereas to sort by mark, you use
        insertion_sort_1(students, key=Student.get_mark)
    This corresponds to the behavior of Python's built-in sorting functions.

    NOTE: THIS IMPLEMENTATION INTENTIONALLY CONTAINS A BUG, 
    WHICH YOUR TESTS ARE SUPPOSED TO DETECT.
    '''
    for i in range(1, len(a)):
        current = a[i]
        j = i
        while j > 0:
            ## In Pytest werft es ein Felher " TypeError: 'str' object is not callable"
            if key(a[j-1]) < key(current):
                break
            else:
                a[j] = a[j-1]                                                  # comment: Current wird nach links verschoben bis das nächst-linke
            j -= 1                                                             #          Element kleiner ist. Es wird also auch mit gleichen
        a[j] = current                                                         #          Elementen vertauscht, wodurch die Implementation nicht
                                                                               #          stabil ist.

def insertion_sort(a, key=lambda x: x,name=True):
                                                                               # comment: Hier sollte ein Docstring sein.
    for i in range(1, len(a)):
        current = a[i]
        j = i
        while j > 0:
            ## In Pytest werft es ein Felher " TypeError: 'str' object is not callable"
            if name is True:
                if a[j - 1].get_name < current.get_name:                       # comment: Um die Schlüssel zu vergleichen sollte key(current), bzw.
                                                                               #          key(a[j-1]) aufgerufen werden. Hier wird stattdessen das
                    break                                                      #          lambda gar nicht verwendet, sondern ein bool übergeben.
                else:                                                          #          Das ist kein generischer code und sollte vermieden werden.
                    a[j] = a[j - 1]
                j -= 1
            else:
                if a[j - 1].get_mark < current.get_mark:                       # comment: Um den bug aus insertion_sort_1 zu beheben. Kann man <= ein-
                    break                                                      #          setzen, oder die Körper von if und else vertauschen und beim
                else:                                                          #          Vergleich > einsetzten.
                    a[j] = a[j - 1]
                j -= 1
        a[j] = current

def merge_sort(a, key=lambda x: x):
    def merge(left, right, key):                                               # comment: Die lokale Funktionsdefinition ist unnötig, da sie nur einmal
        res = []                                                               #          verwendet wird und den Code eher unübersichtlicher macht.
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                j += 1
        res += left[i:] + right[j:]
        return res
    N = len(a)
    if N <= 1:
        return a
    left = a[:N // 2]
    right = a[N // 2:]
    left_sorted = merge_sort(left, key=key)
    right_sorted = merge_sort(right, key=key)
    merged_sorted = merge(left_sorted, right_sorted, key=key)
    return merged_sorted

##################################################################

@pytest.fixture
def arrays():
    '''Create a dictionary holding test data.'''

    data = dict()
    
    # integer arrays
    data['int_arrays'] = [
        [],          # empty array
        [1],          # one element
        [2,1],        # two elements
        [3,2,3,1],    # the array from the exercise text
        [randint(0, 4) for k in range(10)], # 10 random ints
        [randint(0, 4) for k in range(10)]  # another 10 random ints
    ]

    # Student arrays
    data['student_arrays'] = [
       [Student('Adam', 1.3),
        Student('Bert', 2.0),
        Student('Elsa', 1.0),
        Student('Greg', 1.7),
        Student('Jill', 2.7),
        Student('Judy', 3.0),
        Student('Mike', 2.3),
        Student('Patt', 5.0)], # without replicated marks

       [Student('Adam', 1.3),
        Student('Bert', 2.0),
        Student('Elsa', 1.3),
        Student('Greg', 1.0),
        Student('Jill', 1.7),
        Student('Judy', 1.0),
        Student('Mike', 2.3),
        Student('Patt', 1.3)], # with replicated marks, alphabetic

       [Student('Bert', 2.0),
        Student('Mike', 2.3),
        Student('Elsa', 1.3),
        Student('Judy', 1.0),
        Student('Patt', 2.0),
        Student('Greg', 1.0),
        Student('Jill', 1.7),
        Student('Adam', 1.3)] # with replicated marks, random order
    ]
    
    return data

##################################################################
## Mache Funktionen sind mit "test", weil die test Methode muss mit "test_" oder "_test" gestartet,
## damit die Test aufführen könnte.  check_ methode hat solche Funktion nicht.
## Die check Methode dient in diesem Fall nur dazu, dass sie von test_ Funktion benutzt werden.
##Fixtures sind Funktionen, die vor jeder Testfunktion, auf die sie angewendet werden, ablaufen. Fixtures werden verwendet,
# um einige Daten in die Tests einzuspeisen. Anstatt für jeden Test den gleichen Code auszuführen, können wir daher die
# Fixture-Funktion an die Tests anhängen, die dann vor der Ausführung jedes Tests ausgeführt wird und die Daten an den Test zurückgibt.


def test_checks():                                                             # comment: Unnötig, da die beiden aufgerufenen Funktionen den test_ Präfix
    # test that the check_ functions actually find the desired errors          #          haben.
    test_builtin_sort(arrays)                                                  # comment: Verursacht einen Fehler, da hier array als Funktions-Argument
    test_insertion_sort(arrays)                                                #          übergeben wird und in der Funktion nicht als Fixture erkannt wird.
                                                                               # comment: Um die check_ Funktionen zu testen, sollten sie jeweils mit
                                                                               #          inkorrekten Inputs aufgerufen werden, e.g. check_integer_sorting(
                                                                               #          [1, 2], [2, 1]). Um zu überprüfen ob Exceptions aufkommen, kann
                                                                               #          pytest.raises verwendet werden.
                                                                               #          Damit die 3 Bedingungen getestet werden, muss es Inputs mit
                                                                               #              (i) unterschiedlicher Länge,
                                                                               #             (ii) gleicher Länge, aber mit unerschiedlichen Elementen,
                                                                               #            (iii) gleichen Elementen, aber unsortiertem Ergebniss
                                                                               #          geben.

def test_builtin_sort(arrays):
    # test the integer arrays
    for original in arrays['int_arrays']:
        result = list(original)
        check_integer_sorting(original, sorted(result))
    # test the Student arrays
    for original in arrays['student_arrays']:
        result = list(original)
        check_student_sorting(original, sorted(result,key = lambda student:student.mark),"mark")
                                                                               # comment: Statt dem lambda kann die Methode Student.get_mark als key ver-
                                                                               #          wendet werden.
                                                                               # comment: Hier wird der string "mark" übergeben, um später mit attrgetter()
                                                                               #          ein lambda, welches Student.mark zurückgibt, zu erschaffen.
                                                                               #          Einfacher wäre es gewesen, als Argument eine Funktion (oder
                                                                               #          lambda) zu verlangen und hier Student.get_mark zu übergeben.
                                                                               # comment: Es fehlt ein Test ob die Sortierung nach Namen funktioniert. Dies
                                                                               #          kann analog zur Note mit Student.get_name getestet werden.
def test_insertion_sort(arrays):
    # test the integer arrays
    try:
        for original in arrays['int_arrays']:                                  # comment: Statt try sollte pytest.raises verwendet werden, da so der Fehler
            result = list(original)                                            #          erwartetes Verhalten ist.
            insertion_sort_1(result)
            check_integer_sorting(original, result)

        # test the Student arrays
        for original in arrays['student_arrays']:
            result = list(original)
            insertion_sort_1(result, key="mark")                               # comment: key, s.o.
            check_student_sorting(original, result, key="mark")
    except TypeError:
        print("TypeError found")
    finally:
        for original in arrays['int_arrays']:
            result = list(original)
            insertion_sort(result)
            check_integer_sorting(original, result)

        # test the Student arrays
        for original in arrays['student_arrays']:
            result = list(original)
            insertion_sort(result, key="mark")                                 # comment: Test nach Namen, s.o.
            check_student_sorting(original, result, key="mark")


def test_merge_sort(arrays):
    for original in arrays['int_arrays']:
        result = list(original)
        check_integer_sorting(original, merge_sort(result))
        # test the Student arrays
    for original in arrays['student_arrays']:
        result = list(original)
        check_student_sorting(original, merge_sort(result, key=lambda student: student.mark), "mark")
                                                                               # comment: Test nach Namen, s.o.

def test_hierarchical_sort(arrays):
    for original in arrays['student_arrays']:
        result = list(original)
        #sort nach Namen
        result_1 = sorted(original,key = lambda student:student.name)          # comment: Statt sorted() sollte vermutlich eines der eigenen Sortier-
        result_2 = sorted(result_1,key = lambda student:student.mark)          #          Algorithmen verwendet werden.
        for i in len(result_2):                                                # comment: for i in range(result_2 - 1)
            if result_2[i].get_mark == result_2[i+1].get_mark:                 # comment: get_mark()
                assert result_2[i].get_name < result_1.get_name                # comment: result_2[i].get_name() < result_2[i+1].get_name()


def check_integer_sorting(original, result):
    '''Parameter 'original' contains the array before sorting,
    parameter 'result' contains the output of the sorting algorithm.'''
    # check whether the original and the result are of the same length
    if original == []:                                                         # comment: Wenn original leer ist und result Elemente hat, dann sollte der
        pass                                                                   #          Test scheitern. Insofern darf hier nicht pass verwendet werden.
    else:
        out = any(check in original for check in result)
        assert out is True                                                     # comment: out ist eine unnötige Varibale, insbesondere da der Name nicht
                                                                               #          viel aussagt.
                                                                               # comment: "is True" ist überflüssig.
        assert len(original) == len(list(result))
        # assert collections.Counter(original) == collections.Counter(result)
        assert all(result[i] <= result[i + 1] for i in range(len(result) - 1))


def check_student_sorting(original, result, key):
    '''Parameter 'original' contains the array before sorting,
    parameter 'result' contains the output of the sorting algorithm.
    'key' is the attribute defining the order.
    '''
    # check if the both list have the same length
    assert len(original) == len(list(result))

    # check if values are identical
    out = any(check in original for check in result)
    assert out is True
    #assert collections.Counter(original) == collections.Counter(result)

    # sorting

    assert result == sorted(original,key = attrgetter(key))                    # comment: Statt die build-in-Funktion sorted() zu verwenden, reicht es die
                                                                               #          Elemente auf aufsteigende Reihenfolge zu überprüfen. Dazu kann
                                                                               #          der Test aus Zeile 257 modifiziert werden, so dass er key(elem)
                                                                               #          vergleicht.
    # stable check
    f = attrgetter(key)                                                        # comment: Statt f() sollte key() verwendet werden, s.o.
    for i in range(len(result)):
        if f(result[i-1]) != f(result[i]):                                     # comment: Wenn auf Gleichheit geprüft wird und die nachfolgenden Zeilen in
            continue                                                           #          den Körper von if kommen, ist der code leserlicher.
        original_index_i = original.index(result[i])
        original_index_i_minus_one = original.index(result[i-1])
        assert original_index_i_minus_one< original_index_i                    # comment: Leerzeichen bei <, unnötige Variabalen



