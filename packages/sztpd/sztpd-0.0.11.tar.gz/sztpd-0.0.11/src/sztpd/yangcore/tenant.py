# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_W='Unable to parse "input" JSON document: '
_V='malformed-message'
_U='application/yang-data+json'
_T=':tenants/tenant=[^ ]*'
_S=':tenants/tenant=[^/]*/'
_R='" prefix.'
_Q='Top node names must begin with the "'
_P='application'
_O=False
_N='name'
_M=True
_L=':" prefix.'
_K='Non-root data_paths must begin with the "/'
_J=':tenants/tenant/0/'
_I=':tenant'
_H='+'
_G='invalid-value'
_F='text/plain'
_E='protocol'
_D=None
_C=':tenants/tenant='
_B=':'
_A='/'
import re,json,datetime,basicauth
from aiohttp import web
from passlib.hash import sha256_crypt
from .  import dal
from .  import utils
from .rcsvr import RestconfServer
from .handler import RouteHandler
class TenantViewHandler(RouteHandler):
	supported_media_types=_U,
	def __init__(A,native,yl_cb_func):B=native;A.native=B;A.yl_cb_func=yl_cb_func;assert B.dal.app_ns.endswith('-x');A.facade_ns=B.dal.app_ns.replace('-x','-1')
	async def _check_auth(C,request,data_path):
		K='access-denied';J='comment';I='failure';H='outcome';E=request;A={};A['timestamp']=datetime.datetime.utcnow();A['source-ip']=E.remote;A['source-proxies']=list(E.forwarded);A['host']=E.host;A['method']=E.method;A['path']=E.path;L=E.headers.get('AUTHORIZATION')
		if L is _D:A[H]=I;A[J]='No authorization specified in the HTTP header.';await C.native._insert_audit_log_entry(_D,A);B=web.Response(status=401);D=utils.gen_rc_errors(_E,K);B.text=json.dumps(D,indent=2);return B
		G,N=basicauth.decode(L);F=_D
		try:F=await C.native.dal.get_tenant_name_for_admin(G)
		except dal.NodeNotFound as Q:A[H]=I;A[J]='Unknown admin: '+G;await C.native._insert_audit_log_entry(_D,A);B=web.Response(status=401);D=utils.gen_rc_errors(_E,K);B.text=json.dumps(D,indent=2);return B
		if F==_D:A[H]=I;A[J]='Host-level admins cannot use tenant interface ('+G+').';await C.native._insert_audit_log_entry(_D,A);B=web.Response(status=401);D=utils.gen_rc_errors(_E,K);B.text=json.dumps(D,indent=2);return B
		O=_A+C.native.dal.app_ns+_C+F+'/admin-accounts/admin-account='+G+'/password';P=await C.native.dal.handle_get_config_request(O);M=P[C.native.dal.app_ns+':password'];assert M.startswith('$5$')
		if not sha256_crypt.verify(N,M):A[H]=I;A[J]='Password mismatch for admin '+G;await C.native._insert_audit_log_entry(F,A);B=web.Response(status=401);D=utils.gen_rc_errors(_E,K);B.text=json.dumps(D,indent=2);return B
		A[H]='success';await C.native._insert_audit_log_entry(F,A);return F
	async def handle_get_restconf_root(E,request):
		F=request;H=_A;C=await E._check_auth(F,H)
		if type(C)is web.Response:A=C;return A
		else:I=C
		B,J=utils.check_http_headers(F,E.supported_media_types,accept_required=_M)
		if type(B)is web.Response:A=B;return A
		else:assert type(B)==str;D=B;assert D!=_F;G=utils.Encoding[D.rsplit(_H,1)[1]]
		A=web.Response(status=200);A.content_type=D
		if G==utils.Encoding.json:A.text='{\n    "ietf-restconf:restconf" : {\n        "data" : {},\n        "operations" : {},\n        "yang-library-version" : "2019-01-04"\n    }\n}\n'
		else:assert G==utils.Encoding.xml;A.text='<restconf xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">\n    <data/>\n    <operations/>\n    <yang-library-version>2016-06-21</yang-library-version>\n</restconf>\n'
		return A
	async def handle_get_yang_library_version(E,request):
		F=request;H=_A;C=await E._check_auth(F,H)
		if type(C)is web.Response:A=C;return A
		else:I=C
		B,J=utils.check_http_headers(F,E.supported_media_types,accept_required=_M)
		if type(B)is web.Response:A=B;return A
		else:assert type(B)==str;D=B;assert D!=_F;G=utils.Encoding[D.rsplit(_H,1)[1]]
		A=web.Response(status=200);A.content_type=D
		if G==utils.Encoding.json:A.text='{\n  "ietf-restconf:yang-library-version" : "2019-01-04"\n}'
		else:assert G==utils.Encoding.xml;A.text='<yang-library-version xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">2019-01-04</yang-library-version>'
		return A
	async def handle_get_opstate_request(A,request):
		F=request;C,M=utils.parse_raw_path(F._message.path[RestconfServer.len_prefix_operational:]);G=await A._check_auth(F,C)
		if type(G)is web.Response:B=G;return B
		else:H=G
		E,W=utils.check_http_headers(F,A.supported_media_types,accept_required=_M)
		if type(E)is web.Response:B=E;return B
		else:assert type(E)==str;N=E;assert N!=_F;X=utils.Encoding[N.rsplit(_H,1)[1]]
		if C=='/ietf-yang-library:yang-library':B=web.Response(status=200);B.content_type=_U;B.text=A.yl_cb_func();return B
		assert C==_A or C.startswith(_A+A.facade_ns+_B)
		if C==_A:O=_A+A.native.dal.app_ns+_C+H
		else:
			if not C.startswith(_A+A.facade_ns+_B):B=web.Response(status=400);S=_K+A.facade_ns+_L;T=utils.gen_rc_errors(_E,_G,error_message=S);B.text=json.dumps(T,indent=2);return B
			Y,P=C.split(_B,1);assert P!=_D;O=_A+A.native.dal.app_ns+_C+H+_A+P
		Q=dict()
		for R in M.keys():Q[R]=re.sub(_A+A.facade_ns+_B,_A+A.native.dal.app_ns+_C+H+_A,M[R])
		I,D=await A.native.handle_get_opstate_request_lower_half(O,Q)
		if D!=_D:
			assert I.status==200;J={}
			if C==_A:
				for K in D[A.native.dal.app_ns+_I][0].keys():
					if K==_N:continue
					J[A.facade_ns+_B+K]=D[A.native.dal.app_ns+_I][0][K]
			else:L=next(iter(D));assert L.count(_B)==1;U,V=L.split(_B);assert U==A.native.dal.app_ns+'';assert type(D)==dict;assert len(D)==1;J[A.facade_ns+_B+V]=D[L]
			I.text=json.dumps(J,indent=2)
		return I
	async def handle_get_config_request(A,request):
		F=request;B,M=utils.parse_raw_path(F._message.path[RestconfServer.len_prefix_running:]);G=await A._check_auth(F,B)
		if type(G)is web.Response:D=G;return D
		else:H=G
		E,W=utils.check_http_headers(F,A.supported_media_types,accept_required=_M)
		if type(E)is web.Response:D=E;return D
		else:assert type(E)==str;N=E;assert N!=_F;X=utils.Encoding[N.rsplit(_H,1)[1]]
		assert B==_A or B.startswith(_A+A.facade_ns+_B)
		if B==_A:O=_A+A.native.dal.app_ns+_C+H
		else:
			if not B.startswith(_A+A.facade_ns+_B):D=web.Response(status=400);S=_K+A.facade_ns+_L;T=utils.gen_rc_errors(_E,_G,error_message=S);D.text=json.dumps(T,indent=2);return D
			Y,P=B.split(_B,1);assert P!=_D;O=_A+A.native.dal.app_ns+_C+H+_A+P
		Q=dict()
		for R in M.keys():Q[R]=re.sub(_A+A.facade_ns+_B,_A+A.native.dal.app_ns+_C+H+_A,M[R])
		I,C=await A.native.handle_get_config_request_lower_half(O,Q)
		if C!=_D:
			assert I.status==200;J={}
			if B==_A:
				for K in C[A.native.dal.app_ns+_I][0].keys():
					if K==_N:continue
					J[A.facade_ns+_B+K]=C[A.native.dal.app_ns+_I][0][K]
			else:L=next(iter(C));assert L.count(_B)==1;U,V=L.split(_B);assert U==A.native.dal.app_ns+'';assert type(C)==dict;assert len(C)==1;J[A.facade_ns+_B+V]=C[L]
			I.text=json.dumps(J,indent=2)
		return I
	async def handle_post_config_request(B,request):
		D=request;E,K=utils.parse_raw_path(D._message.path[RestconfServer.len_prefix_running:]);H=await B._check_auth(D,E)
		if type(H)is web.Response:A=H;return A
		else:I=H
		F,V=utils.check_http_headers(D,B.supported_media_types,accept_required=_O)
		if type(F)is web.Response:A=F;return A
		else:assert type(F)==str;L=F;assert L!=_F;W=utils.Encoding[L.rsplit(_H,1)[1]]
		if E==_A:M=_A+B.native.dal.app_ns+_C+I
		else:
			if not E.startswith(_A+B.facade_ns+_B):A=web.Response(status=400);Q=_K+B.facade_ns+_L;C=utils.gen_rc_errors(_E,_G,error_message=Q);A.text=json.dumps(C,indent=2);return A
			X,N=E.split(_B,1);assert N!=_D;M=_A+B.native.dal.app_ns+_C+I+_A+N
		O=dict()
		for P in K.keys():O[P]=re.sub(_A+B.facade_ns+_B,_A+B.native.dal.app_ns+_C+I+_A,K[P])
		try:G=await D.json()
		except json.decoder.JSONDecodeError as R:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_V,error_message=_W+str(R));A.text=json.dumps(C,indent=2);return A
		assert type(G)==dict;assert len(G)==1;J=next(iter(G));assert J.count(_B)==1;S,T=J.split(_B)
		if S!=B.facade_ns:A=web.Response(status=400);C=utils.gen_rc_errors(_P,_G,error_message=_Q+B.facade_ns+_R);A.text=json.dumps(C,indent=2);return A
		U={B.native.dal.app_ns+_B+T:G[J]};A=await B.native.handle_post_config_request_lower_half(M,O,U)
		if A.status!=201:
			if _A+B.native.dal.app_ns+_J in A.text:A.text=A.text.replace(_A+B.native.dal.app_ns+_J,_A+B.facade_ns+_B)
			elif _A+B.native.dal.app_ns+_C in A.text:A.text=re.sub(_A+B.native.dal.app_ns+_S,_A+B.facade_ns+_B,A.text);A.text=re.sub(_A+B.native.dal.app_ns+_T,_A+B.facade_ns+_B,A.text)
		return A
	async def handle_put_config_request(B,request):
		F=request;E,M=utils.parse_raw_path(F._message.path[RestconfServer.len_prefix_running:]);I=await B._check_auth(F,E)
		if type(I)is web.Response:A=I;return A
		else:G=I
		H,Y=utils.check_http_headers(F,B.supported_media_types,accept_required=_O)
		if type(H)is web.Response:A=H;return A
		else:assert type(H)==str;N=H;assert N!=_F;Z=utils.Encoding[N.rsplit(_H,1)[1]]
		if E==_A:O=_A+B.native.dal.app_ns+_C+G
		else:
			if not E.startswith(_A+B.facade_ns+_B):A=web.Response(status=400);S=_K+B.facade_ns+_L;C=utils.gen_rc_errors(_E,_G,error_message=S);A.text=json.dumps(C,indent=2);return A
			a,P=E.split(_B,1);assert P!=_D;O=_A+B.native.dal.app_ns+_C+G+_A+P
		Q=dict()
		for R in M.keys():Q[R]=re.sub(_A+B.facade_ns+_B,_A+B.native.dal.app_ns+_C+G+_A,M[R])
		try:D=await F.json()
		except json.decoder.JSONDecodeError as T:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_V,error_message=_W+str(T));A.text=json.dumps(C,indent=2);return A
		if E==_A:
			J={B.native.dal.app_ns+_I:[{_N:G}]}
			for K in D.keys():
				assert K.count(_B)==1;U,V=K.split(_B)
				if U!=B.facade_ns:A=web.Response(status=400);C=utils.gen_rc_errors(_P,_G,error_message=_Q+B.facade_ns+_R);A.text=json.dumps(C,indent=2);return A
				J[B.native.dal.app_ns+_I][0][V]=D[K]
		else:
			assert type(D)==dict;assert len(D)==1;L=next(iter(D));assert L.count(_B)==1;W,X=L.split(_B)
			if W!=B.facade_ns:A=web.Response(status=400);C=utils.gen_rc_errors(_P,_G,error_message=_Q+B.facade_ns+_R);A.text=json.dumps(C,indent=2);return A
			J={B.native.dal.app_ns+_B+X:D[L]}
		A=await B.native.handle_put_config_request_lower_half(O,Q,J)
		if A.status!=201 and A.status!=204:
			if _A+B.native.dal.app_ns+_J in A.text:A.text=A.text.replace(_A+B.native.dal.app_ns+_J,_A+B.facade_ns+_B)
			elif _A+B.native.dal.app_ns+_C in A.text:A.text=re.sub(_A+B.native.dal.app_ns+_S,_A+B.facade_ns+_B,A.text);A.text=re.sub(_A+B.native.dal.app_ns+_T,_A+B.facade_ns+_B,A.text)
		return A
	async def handle_delete_config_request(B,request):
		F=request;C,N=utils.parse_raw_path(F._message.path[RestconfServer.len_prefix_running:]);G=await B._check_auth(F,C)
		if type(G)is web.Response:A=G;return A
		else:H=G
		D,O=utils.check_http_headers(F,B.supported_media_types,accept_required=_O)
		if type(D)is web.Response:A=D;return A
		else:
			assert type(D)==str;E=D
			if E==_F:L=_D
			else:L=utils.Encoding[E.rsplit(_H,1)[1]]
		if C==_A:I=_A+B.native.dal.app_ns+_C+H
		else:
			if not C.startswith(_A+B.facade_ns+_B):
				J=_K+B.facade_ns+_L;A=web.Response(status=400);A.content_type=E
				if E==_F:A.text=J
				else:M=utils.gen_rc_errors(_E,_G,error_message=J);A.text=json.dumps(M,indent=2)
				return A
			P,K=C.split(_B,1);assert K!=_D;I=_A+B.native.dal.app_ns+_C+H+_A+K
		A=await B.native.handle_delete_config_request_lower_half(I)
		if A.status!=204:
			if _A+B.native.dal.app_ns+_J in A.text:A.text=A.text.replace(_A+B.native.dal.app_ns+_J,_A+B.facade_ns+_B)
			elif _A+B.native.dal.app_ns+_C in A.text:A.text=re.sub(_A+B.native.dal.app_ns+_S,_A+B.facade_ns+_B,A.text);A.text=re.sub(_A+B.native.dal.app_ns+_T,_A+B.facade_ns+_B,A.text)
		return A
	async def handle_action_request(A,request):0
	async def handle_rpc_request(A,request):0