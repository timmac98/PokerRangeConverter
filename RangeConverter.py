import re

template = "AA,KK,QQ,JJ,TT,99,88,77,66,55,44,33,22,AKs,AKo,AQs,AQo,AJs,AJo,ATs,ATo,A9s,A9o,A8s,A8o,A7s,A7o,A6s,A6o,A5s,A5o,A4s,A4o,A3s,A3o,A2s,A2o,KQs,KQo,KJs,KJo,KTs,KTo,K9s,K9o,K8s,K8o,K7s,K7o,K6s,K6o,K5s,K5o,K4s,K4o,K3s,K3o,K2s,K2o,QJs,QJo,QTs,QTo,Q9s,Q9o,Q8s,Q8o,Q7s,Q7o,Q6s,Q6o,Q5s,Q5o,Q4s,Q4o,Q3s,Q3o,Q2s,Q2o,JTs,JTo,J9s,J9o,J8s,J8o,J7s,J7o,J6s,J6o,J5s,J5o,J4s,J4o,J3s,J3o,J2s,J2o,T9s,T9o,T8s,T8o,T7s,T7o,T6s,T6o,T5s,T5o,T4s,T4o,T3s,T3o,T2s,T2o,98s,98o,97s,97o,96s,96o,95s,95o,94s,94o,93s,93o,92s,92o,87s,87o,86s,86o,85s,85o,84s,84o,83s,83o,82s,82o,76s,76o,75s,75o,74s,74o,73s,73o,72s,72o,65s,65o,64s,64o,63s,63o,62s,62o,54s,54o,53s,53o,52s,52o,43s,43o,42s,42o,32s,32o"
template = template.split(',')


def pio_to_bk(_range, format_str):
    """
    :param format_str:
    :param _range:
    :return: dictionary?
    """
    r_list = re.split(':|,', _range)
    r_string = ""
    num_floats = 0
    last_hand = '32o'

    for i in range(0, len(r_list)):
        k = i - num_floats
        hand = r_list[i]
        hand_temp = template[k]
        try:
            hand_p1 = r_list[i + 1]
        except IndexError:
            hand_p1 = '1.0'

        if isfloat(hand_p1):
            weight = str(hand_p1)
        else:
            weight = str(1.0)

        if isfloat(hand):
            num_floats += 1
            pass

        # if the two hands are already equal
        elif hand == hand_temp:

            r_string += str_con(hand, weight, format_str)

        # if the suit is not specified eg. AK not AKs
        elif hand in hand_temp:
            hand_s = hand + 's'
            hand_o = hand + 'o'
            r_string += str_con(hand_s, weight, format_str)
            r_string += str_con(hand_o, weight, format_str)

        else:
            j = k
            while hand not in hand_temp:
                if hand_temp in r_string:
                    pass
                else:
                    r_string += str_con(hand_temp, str(0), format_str)
                j += 1
                hand_temp = template[j]

            if hand == hand_temp:
                r_string += str_con(hand, weight, format_str)

            # if the suit is not specified eg. AK not AKs
            else:
                hand_s = hand + 's'
                hand_o = hand + 'o'
                r_string += str_con(hand_s, weight, format_str)
                r_string += str_con(hand_o, weight, format_str)

        if i == len(r_list) - 1:
            if hand == last_hand:
                pass
            else:
                j = k
                while hand_temp != last_hand:
                    if hand_temp in r_string:
                        pass
                    else:
                        r_string += str_con(hand_temp, str(0.0), format_str=format_str)

                    j += 1
                    hand_temp = template[j]
    return r_string[:-1]


def isfloat(value):
    try:
        float(value)
        if '.' in value:
            return True
        else:
            return False
    except ValueError:
        return False


def str_con(h, weight, format_str):
    new_string = format_str[0] + h + format_str[1] + weight + format_str[2]
    return new_string


def convert_range(format='bot', pos=''):
    if format == 'pio':
        pre_str = ''
        mid_str = ':'
        post_str = ','
    else:  ## format == 'bot':
        pre_str = '{"'
        mid_str = '",'
        post_str = '},'

    format_str = [pre_str, mid_str, post_str]
    pos_list = ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']
    act_list = ['', '-2Bet', '-3Bet', '-4Bet', '5Bet','-Flat']
    action = ''
    situation = 'vsUTG_rfi'
    folder = r'vs RFI\vs UTG'

    if format == 'bot':
        output_list = []
        fold_pre = 'vs RFI\\'
        sit_list = ['vs-BTN', 'vs-CO', 'vs-HJ', 'vs-SB', 'vs-UTG']
        for situation in sit_list:
            folder = fold_pre + situation
            for pos in pos_list:
                for action in act_list:
                    file_string = f"C:\\Program Files\\PiioSolver Free\\Free19\\Ranges\\Upswing Exact\\{folder}\\{pos}{action}.txt"
                    try:
                        with open(file_string, 'r') as file:
                            input_range = file.read().replace('\n', '')

                        output_string = f'std::map<std::string, double> {situation}_{pos}{action}' + '{' + str(
                            pio_to_bk(input_range, format_str)) + '};\n'
                        output_string = output_string.replace("-", "_")
                        output_list.append(output_string)
                    except OSError as e:
                        pass

        file1 = open("range_output.txt", "w")
        file1.writelines(output_list)

    else:
        file_string = f"C:\\Program Files\\PiioSolver Free\\Free19\\Ranges\\Upswing Exact\\{folder}\\{pos}.txt"
        with open(file_string, 'r') as file:
            input_range = file.read().replace('\n', '')
        output_string = str(pio_to_bk(input_range, format_str))
        file1 = open("range_output.txt", "w")
        file1.write(output_string)


# convert_range(format='pio', pos='HJ-3Bet')
convert_range(format='bot')
