'''
name:szxxwang
data: 2019-06-19
email:szxxwang@outlook.com
modules:pymongo
This is a dict project!
'''
from socket import *
import os
import time
import signal
import pymysql
import sys

#定义全局变量
DICT_TEXT = './dict.txt'
HOST = '0.0.0.0'
PORT = 8000
ADDR =(HOST,PORT)


# def do_child(c,db):
# 	data = c.recv(1024).decode()
# 	print(data)
# 	if data == 'R':
# 		c.send(b'OK')
# 		do_register(c,db)
# 	elif data == 'L':
# 		do_login()
# 	elif data == 'Q':
# 		do_query()
# 	elif data == 'H':
# 		do_host()

def do_child(c,db):
	while True:
		data = c.recv(128).decode()
		print(c.getpeername(),':',data)
		if not data or data[0] == 'E':
			c.close()
			return
		elif data[0] == 'R':
			do_register(c,db,data)
		elif data[0] == 'L':
			do_login(c,db,data)
		elif data[0] == 'Q':
			do_query(c,db,data)
		elif data[0] == 'H':
			do_hist(c,db,data)


def do_login(c,db,data):
	print('登录操作！')
	l = data.split(' ')
	name = l[1]
	passwd = l[2]
	cursor = db.cursor()
	sql = "select * from user where name='%s'and passwd='%s'"%(name,passwd)
	cursor.execute(sql)
	r = cursor.fetchone()
	if r:
		c.send(b'OK')
	else:
		c.send(b'FAIL')

	
# def do_register(c,db):
# 	while True:

# 		data0 = c.recv(1024).decode()
# 		cursor = db.cursor()

# 		sql = "select * from user where name ='%s'"%data0
# 		cursor.execute(sql)
# 		results = cursor.fetchall()
# 		if not results:
# 			c.send(b'OK')
# 			data1 = c.recv(1024).decode()
# 			sql1 = "insert into user(name,passwd) value('%s','%s')"%(data0,data1)
# 			cursor1 = db.cursor()
# 			cursor1.execute(sql1)
# 			return
# 		else:
# 			c.send(b'NG')
# 			continue

def do_register(c,db,data):
	print('注册操作')
	l = data.split(' ')
	name = l[1]
	passwd = l[2]
	cursor = db.cursor()

	sql = "select * from user where name='%s'"%name
	cursor.execute(sql)
	r = cursor.fetchone()
	if r != None:
		c.send(b'EXISTS')
		return
	sql = "insert into user(name,passwd) values('%s','%s')"%(name,passwd)
	try:
		cursor.execute(sql)
		db.commit()
		c.send(b'OK')
	except:
		db.rollback()
		c.send(b'FAIL')
	else:
		print('%s注册失败'%name)

def do_query(c,db,data):
	print('查询操作')
	l = data.split(' ')
	name = l[1]
	word = l[2]
	cursor = db.cursor()
	def insert_history():
		tm = time.ctime()
		sql = "insert into hist (name,word,time) values ('%s','%s','%s')"%(name,word,tm)
		try:
			cursor.execute(sql)
			db.commit()
		except:
			db.rollback()
	try:
		f = open(DICT_TEXT)
	except:
		c.send(b'FAIL')
		return
	for line in f:
		tmp = line.split(' ')[0]
		if tmp > word:
			c.send(b'FAIL')
			f.close
			return
		elif tmp == word:
			c.send(b'OK')
			time.sleep(0.1)
			c.send(line.encode())
			f.close()
			insert_history()
			return
	c.send(b'FAIL')
	f.close()


def do_hist(c,db,data):
	print('历史记录')
	l = data.split(' ')
	name = l[1]
	cursor = db.cursor()
	sql = "select * from hist where name='%s' order by id desc limit 10"%name
	cursor.execute(sql)
	r = cursor.fetchall()
	if not r:
		c.send(b'FAIL')
		return
	else:
		c.send(b'OK')
	for i in r:
		time .sleep(0.1)
		msg = "%s %s %s"%(i[1],i[2],i[3])
		c.send(msg.encode())
	time.sleep(0.1)
	c.send(b'##')

#流程控制
def main():
	#创建数据库链接
	db = pymysql.connect('localhost','root','lw880814','dict')

	#创建套接字
	s = socket()
	s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	s.bind(ADDR)
	s.listen(5)

	#忽略子进程信号
	signal.signal(signal.SIGCHLD,signal.SIG_IGN)
	while True:
		try:
			c,addr = s.accept()
		except KeyboardInterrupt:
			s.close()
			sys.exit('服务器退出')
		except Exception as e:
			print('error:',e)
			continue
		#创建子进程
		pid = os.fork()
		if pid == 0:
			s.close()
			do_child(c,db)
			sys.exit()
			
		else:
			c.close()
			continue

if __name__ == '__main__':
	main()


