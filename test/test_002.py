from dynamicPip import MirrorManager

mm = MirrorManager()

proxy_list = [
    'pypi.org',
    'mirrors.aliyun.com',
    # TODO unknown host
    # 'unknown.host.com',
    'google.com',
]

mm.mirror_list = proxy_list

# speed_dic, fasted_host = mm.connection_speed_check()
# print(speed_dic)
# print(fasted_host)


print('best mirror is ', mm.get_best_mirror())
