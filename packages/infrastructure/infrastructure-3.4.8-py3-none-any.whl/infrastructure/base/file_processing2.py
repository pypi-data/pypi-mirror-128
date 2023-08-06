# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2021-09-13 17:54:53
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2021-11-17 16:08:09
import os
import platform
import os.path
import json
import django
from AppCooltestHotWheelsService.fox.models.rf_directory_structure import RFDirectoryStructure
from AppCooltestHotWheelsService.application.models.rf_writter import RFWritter
from django.db.models import Q
from django.db import close_old_connections
import time

class FileProcessing(object):
	def __init__(self,rf_project,project_path,env):
		"""
		rf_project : AppHellobikeRfAutoTest
		"""
		self.links = []
		if platform.system() == "Windows":
			self.line = '\\'
		else:
			self.line = '/'

		self.rf_project = rf_project

		self.project_path = project_path

		self.env = env

		# self.rfDirectOB = rfDirectOB

		# self.Q = Q

		# self.close_old_connections = close_old_connections

		self.directStructureList = list(RFDirectoryStructure.objects.filter(~Q(name__icontains='.'),script_name__isnull=True,env=env,valid=True).values_list('structure',flat=True))

		self.scriptStructureList = list(RFDirectoryStructure.objects.filter(script_name__isnull=True,env=env,name__icontains='.',valid=True).values_list('structure',flat=True))

		self.caseNameStructureList = list(RFDirectoryStructure.objects.filter(script_name__isnull=False,env=env,valid=True).values_list('name','structure'))
		# print(self.caseNameStructureList)
		searchOB = RFDirectoryStructure.objects.filter(env=env).order_by('-id')

		if searchOB:
			self.temp = searchOB[0].node_key
		else:
			self.temp = 1


	def __get_root_dir(self,path):
		temp = list()  
		for root, dirs, files in os.walk(path):
			# print(root) #当前目录路径  
			# print(dirs) #当前路径下所有子目录
			# print(files) #当前路径下所有非目录子文件
			for dir in dirs:
				if '.' not in dir:
					temp.append((dir,root + self.line + dir))
			break
			
		return temp

	def __save_directOrScriptName(self,dirName,dirPath,is_script=False):
		temp = dirPath.split(self.line)
		structure = '.'.join(temp[temp.index(self.rf_project) + 1 :])

		if is_script:
			searchOB = RFDirectoryStructure.objects.filter(script_name__isnull=True,name__icontains='.',env=self.env,structure=structure,valid=True)
		else:
			searchOB = RFDirectoryStructure.objects.filter(~Q(name__icontains='.'),script_name__isnull=True,env=self.env,structure=structure,valid=True)
		if not searchOB:
			self.temp += 1
			ob = RFDirectoryStructure(name=dirName,env=self.env,structure=structure,node_key=self.temp)
			ob.save()
			return self.temp
		else:
			if is_script:
				self.scriptStructureList.remove(structure)
			else:
				self.directStructureList.remove(structure)
			return searchOB[0].node_key

	def __save_caseName(self,dirName,dirPath):
		tempStatus = False
		# '/Users/yongfanmao/哈啰mycode/AppHellobikeRfAutoTest/两轮业务C端测试/单车/UAT回归测试收入/单车卡达上限.robot'
		temp = dirPath.split(self.line)
		temp[-1] = temp[-1].split('.')[0]
		structure = '.'.join(temp[temp.index(self.rf_project) + 1 :])
		if 'robot' in dirName:
			with open(dirPath,'r') as f:
				while True:
					line=f.readline()

					if not line:
						break
					if line.startswith('*** Test Cases ***'):
						tempStatus = True
					elif line.startswith('*** Keywords ***'):
						tempStatus = False
					elif line.startswith('*** Variables ***'):
						tempStatus = False
					else:
						pass
					if tempStatus:
						if line.startswith('*** Test Cases ***'):
							continue
						if not line.startswith((' ','\n','#')):
							# print(dirName,line,structure)
							searchOB = RFDirectoryStructure.objects.filter(name=line.strip(),env=self.env,structure=structure,valid=True)
							# try:
							# 	len(searchOB)
							# except:
							# 	django.db.connections.close_all()
							# 	searchOB = RFDirectoryStructure.objects.filter(script_name=dirName,name=line.strip(),env=self.env,structure=structure,valid=True)
							if not searchOB:
								self.temp += 1
								ob = RFDirectoryStructure(script_name=dirName,name=line.strip(),env=self.env,structure=structure,node_key=self.temp)
								ob.save()
								self.links.append((dirName,line.strip(),structure,self.temp))
							else:
								# print((line.strip(),structure))
								self.caseNameStructureList.remove((line.strip(),structure))
								self.links.append((dirName,line.strip(),structure,searchOB[0].node_key))
							del searchOB
						if '[Tags]' in line and not line.startswith(('#')):
							searchOB = RFDirectoryStructure.objects.filter(name=prevLine.strip(),env=self.env,structure=structure,valid=True)
							# print(line,prevLine,structure,searchOB)
							if searchOB:
								searchOB[0].people.clear()
								# tagContent = list(filter(None,line.split(' ')))[1:]
								# line     [Tags]    luoxiuying09632\n
								tagContent = [loop.strip() for loop in line.split(' ')[1:] if loop.strip().isalnum()]
								for people in tagContent:
									wrOb = RFWritter.objects.filter(name=people)
									if wrOb:
										user = wrOb.first()	
									else:
										user = RFWritter.objects.create(name=people)
									searchOB[0].people.add(user)
									del wrOb

							del searchOB

						if not '#' in line:
							prevLine = line
						# close_old_connections()
						
						# time.sleep(1)
						# django.db.connections.close_all()




	def __getLinks(self,path,name=''):
		
		for dir in os.listdir(path):
			dirPath = os.path.join(path, dir)
			if os.path.isdir(dirPath):
				if '.' not in dir:
					if name != '':
						count = self.__save_directOrScriptName(dir,dirPath)
						# print(name,dir,self.temp)
						self.links.append((name,dir,dirPath,count))
					childNode = self.__getLinks(dirPath,dir)
			else:
				if name != '' and not dir.startswith('.'):
					count = self.__save_directOrScriptName(dir,dirPath,is_script=True)
					self.links.append((name,dir,dirPath,count))
					self.__save_caseName(dir,dirPath)
					# self.temp +=1
					# self.links.append((name,dir,dirPath,self.temp))


	def __getRoot(self,path,root):
		
		root_nodes = self.__get_root_dir(path)
		
		for node,path in root_nodes:
			# ('AppHellobikeRfAutoTest', '附件资源', '/Users/yongfanmao/哈啰mycode/AppHellobikeRfAutoTest/附件资源', 65)
			count = self.__save_directOrScriptName(node,path)
			self.links.append((root, node, path, count))


	def __updateValid(self):
		if self.directStructureList:
			RFDirectoryStructure.objects.filter(~Q(name__icontains='.'),script_name__isnull=True,env=self.env,structure__in=self.directStructureList).update(valid=False)
		if self.scriptStructureList:
			RFDirectoryStructure.objects.filter(name__icontains='.',script_name__isnull=True,env=self.env,structure__in=self.scriptStructureList).update(valid=False)
		if self.caseNameStructureList:
			for loop in self.caseNameStructureList:
				RFDirectoryStructure.objects.filter(name=loop[0],env=self.env,structure=loop[1]).update(valid=False)

	def get_directory_tree(self):
		"""
		path 主目录地址
		node 主目录的名称
		"""
		temp = []
		self.__getLinks(self.project_path)
		# print(self.links)
		# import sys
		# sys.exit(1)
		self.__getRoot(self.project_path,self.rf_project)

		tree = self.__get_nodes(self.rf_project)
		# print(json.dumps(tree, indent=4))
		temp.append(tree)

		# print(self.directStructureList,self.scriptStructureList,self.caseNameStructureList)
		self.__updateValid()
		return temp

	def __get_nodes(self,node,path="",id=1):
		d = {}
		if path:
			d['label'] = node
			d['path'] = path
			d['id'] = id
		else:
			d['id'] = 1
			d['label'] = node

		children = self.__get_children(node)
		if children:
			d['children'] = [self.__get_nodes(child[0],child[1],child[2]) for child in children]
		return d

	def __get_children(self,node):
		return [(x[1],x[2],x[3]) for x in self.links if x[0] == node]
					
if __name__ == '__main__':
	f=FileProcessing('AppHellobikeRfAutoTest',"/Users/yongfanmao/哈啰mycode/AppHellobikeRfAutoTest",'uat')
	print(f.get_directory_tree())



