"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    valid = [x for x in paragraphs if select(x)==True]
    if k < len(valid):
               return valid[k]
    else:
               return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    import utils
    def judging(string):
        string = utils.remove_punctuation(string)
        string = utils.lower(string)
        string = utils.split(string)
        #string变成了一个list,里面每个元素是一些被空格分开的字符
        selected_string = [x for x in string if x in topic]
        if len(selected_string) > 0:
            return True
        else:
            return False
        
    return judging
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    iter_num = min(len(typed_words),len(reference_words))
    matching = 0
    for i in range(iter_num):
        if typed_words[i] == reference_words[i]:
            matching += 1
    if len(typed_words):
        return matching/len(typed_words)*100
    else:
        return 0.0

    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return (len(typed)/5) / (elapsed / 60)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if user_word in valid_words:
        return user_word
    else:
        min_diff = min(diff_function(user_word,i,limit) for i in valid_words)
        if min_diff > limit:
            return user_word
        else:
            for word in valid_words:
                if diff_function(user_word,word,limit) == min_diff:
                    return word 


    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    start = list(start)
    goal = list(goal)
    
    def helper(start,goal,limit,times):


        #当start和goal都还有元素
        if start and goal:
            #先判断超过limit次数没有
            if times == limit:
            #当把limit次更换次数用完的时候
            #如果start和goal刚好相等，则return 0, 这样跟limit对比起来的时候肯定不会比limit大
            #如果start和goal不相等，则return 1,这样跟limit 对比起来的时候就会比limit大
            #为什么肯定会比limit大？ 因为此时更改的次数已经刚好在limit边界了，也就是说前面已经加了limit次的1了，
            #这里再加一个1，返回的结果肯定比limit大
                if start == goal:
                    return 0
                else:
                    return 1
                
            
            

            if start[0] == goal[0]:
                start.remove(start[0])
                goal.remove(goal[0])
                return 0 + helper(start,goal,limit,times)
            else:
                start.remove(start[0])
                goal.remove(goal[0])
                return 1 + helper(start,goal,limit,times+1)

        #这里的else指的是如果start或者goal有一个无了，即start和goal长度不相等
        #则找到相差的长度，加到total里面去
        else:
            return max(len(start),len(goal))
            
        
    return helper(start,goal,limit,0)


            
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    original_limit = limit
    if not start and not goal: # Fill in the condition
        # BEGIN
        "*** YOUR CODE HERE ***"
        return 0
        # END

    elif not start or not goal: # Feel free to remove or add additional cases
        # BEGIN
        "*** YOUR CODE HERE ***"
        return abs(len(start) - len(goal))
        # END
        
    elif limit ==0 and start !=goal:
        return original_limit + 1

    elif start[0] == goal[0]:
        return pawssible_patches(start[1:],goal[1:],limit)

    else:
        add_diff = pawssible_patches(start,goal[1:],limit - 1) # Fill in these lines
        remove_diff = pawssible_patches(start[1:],goal,limit - 1)
        substitute_diff = pawssible_patches(start[1:],goal[1:], limit - 1)
        
        return min(add_diff,remove_diff,substitute_diff) +1
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END

def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    #①：calculate progress
    #②：create a dictionary
    #③：send the report with 'send' function
    
    #①：calculate progress
    stop = False
    correct_words = 0
    total = len(prompt)

    while prompt and typed and stop == False:
        if typed[0] == prompt[0]:
            typed = typed[1:]
            prompt = prompt[1:]
            correct_words += 1
        else:
            stop = True
    progress = correct_words / total
    
    #②：create a dictionary
    report = {'id': user_id, 
              'progress': progress}
    send(report)
    
    #③：send the report with 'send' function
    return progress

    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    #①：第一个列表装words
    #②:第二个列表装每个player的time
    
    #①：装words的列表不需要构建，直接返回参数words
    #②：装每个player的time的列表
    time_for_all_player = []
    
    for player in times_per_player:
        time_for_one_player = []
        i = 0
        while i < len(words):
            word_time = player[i+1] - player[i]
            time_for_one_player.append(word_time)
            i += 1
        time_for_all_player.append(time_for_one_player)

    return game(words,time_for_all_player)

    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    words = all_words(game)
    time = all_times(game)
    
    
    #创建装结果的list
    result = list()
    for i in player_indices:
        result.append(list())
        
    #一个个Word去遍历
    for word in word_indices:
        min_time_for_this_word = min(time[i][word] for i in player_indices)
        find = False
        for player in player_indices:
            if time[player][word]==min_time_for_this_word and not find: #这个player的这个word的时间是否是min
                result[player].append(words[word])
                find = True
    return result
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = True  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
