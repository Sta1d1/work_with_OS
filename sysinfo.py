import subprocess
import datetime


def get_inform():

    users = '$1'
    process = '$2'
    mem = '$4'
    cpu = '$3'
    proc_name = '$11'

    ps = subprocess.Popen(('ps', 'aux'), stdout=subprocess.PIPE)
    output = subprocess.check_output(( 'awk', "{print " + users + "," + process + "," + mem + "," + cpu + "," + proc_name + "}" ), stdin=ps.stdout, encoding='UTF-8')

    res_list = []
    with open('tmp.txt', 'w') as file:
        file.write(output)
        file.close()

        with open('tmp.txt', 'r') as file:
            for line in file:
                n = line.split(' ')
                res_list.append(n)
    res_list = res_list[1::]


    users = []
    for user in res_list:
        if user[0] not in users:
            users.append(user[0])
    string_users = ''
    for user2 in users:
        string_users +=  '"' + user2 + '", '
    res_users = 'Пользователи системы: ' + string_users
    res_users = res_users[:-2]


    counter_proc = 0
    for count in res_list:
        counter_proc += 1
    res_counter_proc = 'Процессов запущено: ' + str(counter_proc)


    u_dict = {}
    for u in users:
        u_dict[u] = 0
    for u_proc in users:
        for block in res_list:
            if block[0] == u_proc:
                u_dict[u_proc] = u_dict[u_proc] + 1
    res_u_dict = ''
    for t in u_dict:
        res_u_dict += t + ': ' + str(u_dict[t]) + '\n'
    res_u_dict = 'Пользовательских процессов: \n' +  res_u_dict


    mem_info = 0
    for mem in res_list:
        mem_info += float(str(mem[2]).replace('\n', ''))
    res_mem_info = 'Всего памяти используется: ' + str(mem_info) + '%'


    cpu_info = 0
    for cpu in res_list:
        cpu_info += float(str(cpu[3]).replace('\n', ''))
    res_cpu_info = 'Всего CPU используется: ' + str(cpu_info) + '%'


    source = []
    for item in res_list:
        source.append(item[2])
    max_mem = max(source)
    proc_name = ''
    text = 'Больше всего MEM использует: '
    for item2 in res_list:
        if item2[2] == max_mem:
            proc_name = item2[4]
            break
    res_max_mem = text + proc_name.replace('\n', '')[:20]


    source = []
    for item in res_list:
        source.append(item[3])
    max_cpu = max(source)
    proc_name = ''
    text = 'Больше всего CPU использует: '
    for item2 in res_list:
        if item2[3] == max_cpu:
            proc_name = item2[4]
            break
    res_max_cpu = text + proc_name.replace('\n', '')[:20]


    with open('tmp.txt', 'w') as file:
        file.write(
            res_users + '\n' + 
            res_counter_proc + '\n' +
            res_u_dict + '\n' +
            res_mem_info + '\n' +
            res_cpu_info + '\n' +
            res_max_mem + '\n' +
            res_max_cpu + '\n'
        )

    current_time = datetime.datetime.now()
    current_time = current_time.ctime()
    current_time = current_time.replace(' ', '-')
    current_time = current_time.replace(':', '-')
    file_name = current_time + '-' + 'result.txt'
    subprocess.Popen(('mv', 'tmp.txt', file_name))


if __name__ == '__main__':
    get_inform()
