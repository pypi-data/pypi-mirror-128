# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_W='Unrecognized member: '
_V='Query parameters are only supported for "list" and "leaf-list" nodes.'
_U=') is not a sibling of the target node ('
_T='Unrecognized schema path for "point" node: '
_S='The query parameter "point" is required when the "insert" parameter is "'
_R='Unrecognized "insert" query parameter value: '
_Q='" is not recognized.'
_P='The parameter "'
_O='The top-level node-identifier must be prefixed by a namespace followed by a colon.'
_N='Parent data node ('
_M='Input document must contain at least one top-level node.'
_L='Data node ('
_K='Unrecognized schema path: '
_J='Invalid data path: '
_I='Validation failed: '
_H='The "point" node ('
_G='after'
_F='before'
_E=') does not exist.'
_D=True
_C='insert'
_B='point'
_A='/'
import json,yangson,asyncio
from urllib.parse import quote
class NodeAlreadyExists(Exception):0
class NodeNotFound(Exception):0
class ParentNodeNotFound(Exception):0
class InvalidDataPath(Exception):0
class InvalidInputDocument(Exception):0
class UnrecognizedInputNode(Exception):0
class UnrecognizedQueryParameter(Exception):0
class MissingQueryParameter(Exception):0
class InvalidQueryParameter(Exception):0
class NonexistentSchemaNode(Exception):0
class ValidationFailed(Exception):0
class ValidationLayer:
	def __init__(A,dm,dal):
		A.dm=dm;A.dal=dal;C=asyncio.get_event_loop();D=A.dal.handle_get_config_request(_A);E=C.run_until_complete(D);A.inst=A.dm.from_raw(E)
		try:A.inst.validate()
		except yangson.exceptions.SchemaError as B:assert str(B).startswith('{/} missing-data: expected');assert str(B).endswith(":admin-accounts'")
	async def handle_get_config_request(C,data_path,query_dict):
		A=data_path;assert A!='';assert not(A!=_A and A[-1]==_A)
		try:E=C.dm.parse_resource_id(A)
		except yangson.exceptions.UnexpectedInput as B:raise InvalidDataPath(_J+str(B))
		except yangson.exceptions.NonexistentSchemaNode as B:raise NonexistentSchemaNode(_K+A)
		try:D=C.inst.goto(E)
		except yangson.exceptions.NonexistentInstance as B:raise NodeNotFound(_L+A+_E)
		if type(D)!=yangson.instance.ArrayEntry and isinstance(D.schema_node,yangson.schemanode.SequenceNode):raise InvalidDataPath("RFC 8040 doesn't acknowledge 'list' or 'list-list' nodes as resource targets.")
	async def handle_post_config_request(G,data_path,query_dict,request_body):
		W="' must contain one element.";V="Input 'list' node '";U="' not a 'list' node.";T="Input node '";R=None;H=data_path;C=request_body;B=query_dict
		if len(C)<1:raise InvalidInputDocument(_M)
		if len(C)>1:raise InvalidInputDocument('Input document must not have more than one top-level node.')
		try:X=G.dm.parse_resource_id(H)
		except yangson.exceptions.NonexistentSchemaNode as D:raise NonexistentSchemaNode('Unrecognized schema path for parent node: '+H)
		try:I=G.inst.goto(X)
		except yangson.exceptions.NonexistentInstance as D:raise ParentNodeNotFound(_N+H+_E)
		A=next(iter(C))
		if':'not in A:raise InvalidInputDocument(_O)
		Y,F=A.split(':');M=I.schema_node;J=M.get_child(F,Y)
		if J is R:raise UnrecognizedInputNode('Input document contains unrecognized top-level node.')
		if not M.ns is R:assert M.ns==J.ns
		if isinstance(J,yangson.schemanode.SequenceNode):
			if type(J)==yangson.schemanode.ListNode:
				Z=J.keys[0];a=Z[0]
				if type(C[A])!=list:raise InvalidInputDocument(T+F+U)
				if len(C[A])!=1:raise InvalidInputDocument(V+F+W)
				N=C[A][0];Q=N[a]
			elif type(J)==yangson.schemanode.LeafListNode:
				if type(C[A])!=list:raise InvalidInputDocument(T+F+U)
				if len(C[A])!=1:raise InvalidInputDocument(V+F+W)
				N=C[A][0];Q=C[A][0]
			else:raise AssertionError('Logic cannot reach this point')
			if H==_A:E=A;K=_A+E+'='+quote(Q,safe='')
			else:E=F;K=H+_A+E+'='+quote(Q,safe='')
			try:b=G.dm.parse_resource_id(K)
			except yangson.exceptions.NonexistentSchemaNode as D:raise NonexistentSchemaNode('Unrecognized schema path for insertion node: '+K)
			try:G.inst.goto(b)
			except yangson.exceptions.NonexistentInstance as D:pass
			else:raise NodeAlreadyExists('Child data node ('+K+') already exists.')
			for O in B:
				if O not in(_C,_B):raise UnrecognizedQueryParameter(_P+O+_Q)
				if O==_C:
					if B[_C]not in('first',_F,_G,'last'):raise InvalidQueryParameter(_R+B[_C])
					if B[_C]in(_F,_G):
						if _B not in B:raise MissingQueryParameter(_S+insert+'"')
				if O==_B:
					try:c=G.dm.parse_resource_id(B[_B])
					except yangson.exceptions.NonexistentSchemaNode as D:raise NonexistentSchemaNode(_T+B[_B])
					try:G.inst.goto(c)
					except yangson.exceptions.NonexistentInstance as D:raise InvalidQueryParameter(_H+B[_B]+_E)
					if H!=B[_B].rsplit(_A,1)[0]:raise InvalidQueryParameter(_H+B[_B]+_U+K+').')
			try:L=I[E]
			except yangson.exceptions.NonexistentInstance:L=I.put_member(E,yangson.instvalue.ArrayValue([]))
			assert isinstance(L.schema_node,yangson.schemanode.SequenceNode)
			if len(L.value)==0:
				try:d=L.update([N],raw=_D)
				except yangson.exceptions.RawMemberError as D:raise UnrecognizedInputNode('Incompatable node data. '+str(D))
				P=d.up()
			else:e=L[-1];P=e.insert_after(N,raw=_D).up()
		else:
			if len(B)>0 and len(B)==1 and'sleep'not in B:raise UnrecognizedQueryParameter(_V)
			if H==_A:E=A
			else:E=F
			if E in I:raise NodeAlreadyExists('Node "'+E+'" already exists.')
			try:
				if M.ns==R:P=I.put_member(A,C[A],raw=_D).up()
				else:P=I.put_member(F,C[A],raw=_D).up()
			except yangson.exceptions.RawMemberError as D:raise UnrecognizedInputNode(_W+str(D))
		S=P.top()
		try:S.validate()
		except Exception as D:raise ValidationFailed(_I+str(D))
		G.inst2=S
	async def handle_put_config_request(C,data_path,query_dict,request_body):
		E=request_body;D=data_path;A=query_dict;assert D!='';assert not(D!=_A and D[-1]==_A)
		if len(E)<1:raise InvalidInputDocument(_M)
		I=next(iter(E))
		if':'not in I:raise InvalidInputDocument(_O)
		try:L=C.dm.parse_resource_id(D)
		except yangson.exceptions.UnexpectedInput as B:raise InvalidDataPath(_J+str(B))
		except yangson.exceptions.NonexistentSchemaNode as B:raise NonexistentSchemaNode(_K+D)
		try:F=C.inst.goto(L)
		except yangson.exceptions.NonexistentInstance as B:
			O=C.inst.raw_value();G=D.rsplit(_A,1)[0]
			if G=='':G=_A
			M=C.dm.parse_resource_id(G)
			try:F=C.inst.goto(M)
			except yangson.exceptions.NonexistentInstance as B:raise ParentNodeNotFound(_N+G+') does not exist. '+str(B))
			await C.handle_post_config_request(G,A,E);return
		if isinstance(F.schema_node,yangson.schemanode.SequenceNode):
			for H in A:
				if H not in(_C,_B):raise UnrecognizedQueryParameter(_P+H+_Q)
				if H==_C:
					if A[_C]not in('first',_F,_G,'last'):raise InvalidQueryParameter(_R+A[_C])
					if A[_C]in(_F,_G):
						if _B not in A:raise MissingQueryParameter(_S+insert+'"')
				if H==_B:
					try:N=C.dm.parse_resource_id(A[_B])
					except yangson.exceptions.NonexistentSchemaNode as B:raise NonexistentSchemaNode(_T+A[_B])
					try:C.inst.goto(N)
					except yangson.exceptions.NonexistentInstance as B:raise InvalidQueryParameter(_H+A[_B]+_E)
					if D.rsplit(_A,1)[0]!=A[_B].rsplit(_A,1)[0]:raise InvalidQueryParameter(_H+A[_B]+_U+D+').')
		elif len(A)>0 and len(A)==1 and'sleep'not in A:raise UnrecognizedQueryParameter(_V)
		try:
			if D==_A:J=F.update(E,raw=_D)
			elif isinstance(F.schema_node,yangson.schemanode.SequenceNode):J=F.update(E[I][0],raw=_D)
			else:J=F.update(E[I],raw=_D)
		except yangson.exceptions.RawMemberError as B:raise UnrecognizedInputNode(_W+str(B))
		except Exception as B:raise NotImplementedError(str(type(B))+' = '+str(B))
		K=J.top()
		try:K.validate()
		except Exception as B:raise ValidationFailed(_I+str(B))
		C.inst2=K
	async def handle_delete_config_request(C,data_path):
		B=data_path;assert B!=''
		if B==_A:E=RootNode(ObjectValue({}),C.inst.schema_node,datetime.now())
		else:
			try:J=C.dm.parse_resource_id(B)
			except yangson.exceptions.NonexistentSchemaNode as F:raise NonexistentSchemaNode('Unrecognized schema path for data node: '+B)
			try:D=C.inst.goto(J)
			except yangson.exceptions.NonexistentInstance as F:raise NodeNotFound(_L+B+_E)
			H=D.up()
			if type(D)==yangson.instance.ArrayEntry:
				A=H.delete_item(D.index)
				if len(A.value)==0:
					G=A.up()
					if isinstance(G.schema_node,yangson.schemanode.SequenceNode):I=G.delete_item(A.index);raise NotImplementedError('tested? list inside a list...')
					else:I=G.delete_item(A.name)
					A=I
			else:A=H.delete_item(D.name)
			E=A.top()
		try:E.validate()
		except Exception as F:raise ValidationFailed(_I+str(F))
		C.inst2=E