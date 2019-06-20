#!/usr/bin/python3
#coding = utf-8
from socket import *
import sys
import getpass

# def do_register(s):
# 	s.send(b'R')
# 	data = s.recv(1024)
# 	if data == 'OK':
# 		while True:
# 			name = input('please input the user name:')
# 			s.send(name.encode())
# 			data1 = s.recv(1024)
# 			if data1 == 'OK':
# 				while True:
# 					pwd = input('please input the password:')
# 					if len(pwd) < 6:
# 						print('your password is illegal')
# 					else:
# 						s.send(pwd.encode())
# 						return

# 			else:
# 				print('The user name exist!')
# 				continue
def do_query(s,name):
	while True:
		word = input('word')
		if word == '##':
			break
		msg = 'Q {} {}'.format(name,word)
		s.send(msg.encode())
		data = s.recv(128).decode()
		if data == 'OK':
			data = s.recv(2048).decode()
			print(data)
		else:
			print('没有查到该单词！')
def do_hist(s,name):
	msg = 'H {}'.format(name)
	s.send(msg.encode())
	data = s.recv(128).decode()
	if data == 'OK':
		while True:
			data = s.recv(1024).decode()
			if data == '##':
				break
			print(data)
	else:
		print('没有历史记录！')
def do_register(s):
	while True:
		name = input('User name:')
		password = getpass.getpass('please input the password:')
		password1 = getpass.getpass('one more time :')
		if (' 'in name ) or (' 'in password):
			print('用户名和密码不能有空格！')
			continue
		if password != password1:
			print('两次密码不一致！')
			continue
		msg = 'R {} {}'.format(name,password)
		s.send(msg.encode())
		data = s.recv(128).decode()
		if data == 'OK':
			return 0
		elif data == 'EXISTS':
			return 1
		else:
			return 2
# def do_login(s):
# 	while True:
# 		name = input('please input your name :')
# 		password = input('please input your password:')
# 		msg = 'L {} {}'.format(name,password)
# 		s.send(msg.encode())
# 		data = s.recv(128).decode()
# 		if data == 'OK':
# 			print('登录成功!')
# 			return 0
# 		elif data == 'NG':
# 			print('用户名不存在，请重新输入！')
# 			continue
# 		else:
# 			print('用户名或密码输入错误，请重新输入！')
# 			continue
def login(s,name):
	while True:
		print('''
			======查询界面=======
			1.查词  2.查询历史记录 3.退出
			''')
		cmd = int(input('请输入选项：'))
		if cmd not in[1,2,3]:
			print('请输入正确命令！')
			sys.stdin.flush()
			continue
		elif cmd == 1:
			do_query(s,name)
		elif cmd == 2:
			do_hist(s,name)
		elif cmd == 3:
			s.close()
			break


def do_login(s):
	name = input('User:')
	password = getpass.getpass()
	msg = "L {} {}".format(name,password)
	s.send(msg.encode())
	data = s.recv(128).decode()
	if data == 'OK':
		return name 
	else:
		return None

#创建网络链接
def main():
	if len(sys.argv) < 3:
		print('argv is error!')
		return
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	s = socket()
	try:
		s.connect((HOST,PORT))
	except Exception as e:
		print(e)
		return
	while True:
		print('''
			======Welcome========
			--1.注册 2.登录 3.退出--
			=====================
			''')
		try:
			cmd = int(input('请输入命令：'))
		except Exception as e:
			print('命令错误！')
			continue
		if cmd not in[1,2,3]:
			print('请输入正确命令！')
			sys.stdin.flush()
			continue
		elif cmd ==1:
			 r = do_register(s)
			 if r == 0:
			 	print('注册成功！')
			 elif r ==1:
			 	print('用户存在')
			 else:
			 	print('注册失败')
		elif cmd == 2:
			name = do_login(s)
			if name:
				print('登录成功')
				login(s,name)
				
			else:
				print('用户名或密码输入错误，请重新输入！')
		elif cmd == 3:
			s.send(b'E')
			s.close()
			sys.exit('Thank you bye!')
			

if __name__ == '__main__':
	main()