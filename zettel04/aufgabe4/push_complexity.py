import timeit
import matplotlib.pyplot as plt

setup_fast = ('from DequeArray import DequeArray;'
              'a = DequeArray()')
setup_slow = ('from DequeArray import SlowDequeArray;'
              'a = SlowDequeArray()')
command = 'a.push(5435980)'

repetions = range(0, 1200, 15)
slowdeqtimes = []
fastdeqtimes = []

for i in repetions:
    # taking min of 10 runs each time to reduce variance caused by other procceses
    slowdeqtimes.append(min(timeit.repeat(command, setup_slow, repeat=10, number=i)))
    fastdeqtimes.append(min(timeit.repeat(command, setup_fast, repeat=10, number=i)))


fig = plt.figure(figsize=(20, 10))

plt.suptitle('Comparison between DequeArray implementations', fontsize=20)
plt.figtext(0.5, 0.9, 'DequeArray doubles its capacity each time it is reached.\n'
            'SlowDequeArray increases its capacity by one each time it is reached.',
            fontsize=15, ha='center')

plt.subplot(121)
plt.ylabel('time in s')
plt.xlabel('.push() repetions')
plt.plot(repetions, fastdeqtimes, label='DequeArray')
plt.plot(repetions, slowdeqtimes, label='SlowDequeArray')
plt.legend()

plt.subplot(122)
plt.ylabel('time in s')
plt.xlabel('.push() repetions')
plt.plot(repetions, fastdeqtimes, label='DequeArray')

plt.axvline(x=2**4, color='green', linestyle='dashed', label='Powers of 2')
for xc in [2**i for i in range(5, 11)]:
    plt.axvline(x=xc, color='green', linestyle='dashed')

plt.legend()

plt.show()


