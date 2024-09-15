from functions import search_project,update,init_records,list_noRecord,clear

def loop() -> bool:
    print(
'''
1. 更新
2. 搜索
3. 退出
4. 自动补全记录
5. 展示未在记录中的模组
6. 清除多余记录
''')
    t=input()
    match t:
        case '1':
            update()
        case '2':
            search_project()
        case '3':
            return False
        case '4':
            init_records()
        case '5':
            list_noRecord()
        case '6':
            clear()
    return True

def main() -> None:
    while loop():
        ...

if __name__=="__main__":
    main()

