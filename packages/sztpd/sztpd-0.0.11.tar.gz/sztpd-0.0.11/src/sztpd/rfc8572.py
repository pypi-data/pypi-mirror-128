# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_Ab='Returning an RPC-error provided by callback (NOTE: RPC-error != exception, hence a normal exit).'
_Aa='Unrecognized error-tag: '
_AZ='partial-operation'
_AY='operation-failed'
_AX='rollback-failed'
_AW='data-exists'
_AV='resource-denied'
_AU='lock-denied'
_AT='unknown-namespace'
_AS='bad-element'
_AR='unknown-attribute'
_AQ='bad-attribute'
_AP='missing-attribute'
_AO='exception-thrown'
_AN='functions'
_AM='callback-details'
_AL='from-device'
_AK='identity-certificate'
_AJ='source-ip-address'
_AI='mode-0 == no-sn'
_AH='"ietf-sztp-bootstrap-server:input" is missing.'
_AG='/ietf-sztp-bootstrap-server:report-progress'
_AF='Resource does not exist.'
_AE='Requested resource does not exist.'
_AD=':log-entry'
_AC='/devices/device='
_AB=':devices/device='
_AA='2021-02-24'
_A9='2019-04-30'
_A8='urn:ietf:params:xml:ns:yang:ietf-yang-types'
_A7='ietf-yang-types'
_A6='module-set-id'
_A5='ietf-yang-library:modules-state'
_A4='application/yang-data+xml'
_A3='webhooks'
_A2='callout-type'
_A1='passed-input'
_A0='ssl_object'
_z='access-denied'
_y='/ietf-sztp-bootstrap-server:get-bootstrapping-data'
_x='Parent node does not exist.'
_w='Resource can not be modified.'
_v='2013-07-15'
_u='webhook'
_t='exited-normally'
_s='opaque'
_r='function'
_q='plugin'
_p='serial-number'
_o='rpc-supported'
_n='data-missing'
_m='Unable to parse "input" document: '
_l='import'
_k='application/yang-data+json'
_j='operation-not-supported'
_i=':device'
_h='Content-Type'
_g='malformed-message'
_f=False
_e=':tenants/tenant='
_d='implement'
_c='callback-results'
_b='callback'
_a='invalid-value'
_Z='unknown-element'
_Y=True
_X='application'
_W='path'
_V='method'
_U='source-ip'
_T='timestamp'
_S='0'
_R='conformance-type'
_Q='namespace'
_P='revision'
_O='ietf-sztp-bootstrap-server:input'
_N='error-tag'
_M='error'
_L='protocol'
_K='text/plain'
_J='ietf-restconf:errors'
_I='name'
_H=':dynamic-callout'
_G='+'
_F='return-code'
_E='dynamic-callout'
_D='error-returned'
_C=None
_B='event-details'
_A='/'
import os,json,base64,pprint,asyncio,aiohttp,yangson,datetime,basicauth,urllib.parse,pkg_resources
from aiohttp import web
from pyasn1.type import univ
from pyasn1_modules import rfc5652
from passlib.hash import sha256_crypt
from pyasn1.codec.der.encoder import encode as encode_der
from pyasn1.codec.der.decoder import decode as der_decoder
from certvalidator import CertificateValidator,ValidationContext,PathBuildingError
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from .yangcore import dal
from .yangcore import utils
from .yangcore.native import Read
from .yangcore.dal import DataAccessLayer
from .yangcore.rcsvr import RestconfServer
from .yangcore.handler import RouteHandler
from .  import yl
class RFC8572ViewHandler(RouteHandler):
	len_prefix_running=len(RestconfServer.root+'/ds/ietf-datastores:running');len_prefix_operational=len(RestconfServer.root+'/ds/ietf-datastores:operational');len_prefix_operations=len(RestconfServer.root+'/operations');id_ct_sztpConveyedInfoXML=rfc5652._buildOid(1,2,840,113549,1,9,16,1,42);id_ct_sztpConveyedInfoJSON=rfc5652._buildOid(1,2,840,113549,1,9,16,1,43);supported_media_types=_k,_A4;yl4errors={_A5:{_A6:'TBD','module':[{_I:_A7,_P:_v,_Q:_A8,_R:_l},{_I:'ietf-restconf',_P:'2017-01-26',_Q:'urn:ietf:params:xml:ns:yang:ietf-restconf',_R:_d},{_I:'ietf-netconf-acm',_P:'2018-02-14',_Q:'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',_R:_l},{_I:'ietf-sztp-bootstrap-server',_P:_A9,_Q:'urn:ietf:params:xml:ns:yang:ietf-sztp-bootstrap-server',_R:_d},{_I:'ietf-yang-structure-ext',_P:'2020-06-22',_Q:'urn:ietf:params:xml:ns:yang:ietf-yang-structure-ext',_R:_d},{_I:'ietf-sztp-csr',_P:_AA,_Q:'urn:ietf:params:xml:ns:yang:ietf-sztp-csr',_R:_d},{_I:'ietf-crypto-types',_P:_AA,_Q:'urn:ietf:params:xml:ns:yang:ietf-crypto-types',_R:_d}]}};yl4conveyedinfo={_A5:{_A6:'TBD','module':[{_I:_A7,_P:_v,_Q:_A8,_R:_l},{_I:'ietf-inet-types',_P:_v,_Q:'urn:ietf:params:xml:ns:yang:ietf-inet-types',_R:_l},{_I:'ietf-sztp-conveyed-info',_P:_A9,_Q:'urn:ietf:params:xml:ns:yang:ietf-sztp-conveyed-info',_R:_d}]}}
	def __init__(A,dal,mode,yl,nvh):C='sztpd';A.dal=dal;A.mode=mode;A.nvh=nvh;B=pkg_resources.resource_filename(C,'yang');A.dm=yangson.DataModel(json.dumps(yl),[B]);A.dm4conveyedinfo=yangson.DataModel(json.dumps(A.yl4conveyedinfo),[B]);D=pkg_resources.resource_filename(C,'yang4errors');A.dm4errors=yangson.DataModel(json.dumps(A.yl4errors),[D,B])
	async def _insert_bootstrapping_log_entry(A,device_id,bootstrapping_log_entry):
		E='/bootstrapping-log';B=device_id
		if A.mode==_S:C=_A+A.dal.app_ns+':device/bootstrapping-log'
		elif A.mode=='1':C=_A+A.dal.app_ns+_AB+B[0]+E
		elif A.mode=='x':C=_A+A.dal.app_ns+_e+B[1]+_AC+B[0]+E
		D={};D[A.dal.app_ns+_AD]=bootstrapping_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def _insert_audit_log_entry(A,tenant_name,audit_log_entry):
		B=tenant_name
		if A.mode==_S or A.mode=='1'or B==_C:C=_A+A.dal.app_ns+':audit-log'
		elif A.mode=='x':C=_A+A.dal.app_ns+_e+B+'/audit-log'
		D={};D[A.dal.app_ns+_AD]=audit_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def handle_get_restconf_root(D,request):
		C=request;J=_A;F=await D._check_auth(C,J)
		if type(F)is web.Response:A=F;return A
		else:H=F
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=C.remote;B[_V]=C.method;B[_W]=C.path;E,K=utils.check_http_headers(C,D.supported_media_types,accept_required=_Y)
		if type(E)is web.Response:A=E;L=K;B[_F]=A.status;B[_D]=L;await D._insert_bootstrapping_log_entry(H,B);return A
		else:assert type(E)==str;G=E;assert G!=_K;I=utils.Encoding[G.rsplit(_G,1)[1]]
		A=web.Response(status=200);A.content_type=G
		if I==utils.Encoding.json:A.text='{\n    "ietf-restconf:restconf" : {\n        "data" : {},\n        "operations" : {},\n        "yang-library-version" : "2019-01-04"\n    }\n}\n'
		else:assert I==utils.Encoding.xml;A.text='<restconf xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">\n    <data/>\n    <operations/>\n    <yang-library-version>2016-06-21</yang-library-version>\n</restconf>\n'
		B[_F]=A.status;await D._insert_bootstrapping_log_entry(H,B);return A
	async def handle_get_yang_library_version(D,request):
		C=request;J=_A;F=await D._check_auth(C,J)
		if type(F)is web.Response:A=F;return A
		else:H=F
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=C.remote;B[_V]=C.method;B[_W]=C.path;E,K=utils.check_http_headers(C,D.supported_media_types,accept_required=_Y)
		if type(E)is web.Response:A=E;L=K;B[_F]=A.status;B[_D]=L;await D._insert_bootstrapping_log_entry(H,B);return A
		else:assert type(E)==str;G=E;assert G!=_K;I=utils.Encoding[G.rsplit(_G,1)[1]]
		A=web.Response(status=200);A.content_type=G
		if I==utils.Encoding.json:A.text='{\n  "ietf-restconf:yang-library-version" : "2019-01-04"\n}'
		else:assert I==utils.Encoding.xml;A.text='<yang-library-version xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">2019-01-04</yang-library-version>'
		B[_F]=A.status;await D._insert_bootstrapping_log_entry(H,B);return A
	async def handle_get_opstate_request(C,request):
		D=request;E=D.path[C.len_prefix_operational:];E=_A;G=await C._check_auth(D,E)
		if type(G)is web.Response:A=G;return A
		else:I=G
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;F,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_Y)
		if type(F)is web.Response:A=F;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(I,B);return A
		else:assert type(F)==str;H=F;assert H!=_K;J=utils.Encoding[H.rsplit(_G,1)[1]]
		if E=='/ietf-yang-library:yang-library'or E==_A or E=='':A=web.Response(status=200);A.content_type=_k;A.text=getattr(yl,'sbi_rfc8572')()
		else:A=web.Response(status=404);A.content_type=H;J=utils.Encoding[A.content_type.rsplit(_G,1)[1]];K=utils.gen_rc_errors(_L,_Z,error_message=_AE);N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,N);B[_D]=K
		B[_F]=A.status;await C._insert_bootstrapping_log_entry(I,B);return A
	async def handle_get_config_request(C,request):
		D=request;F=D.path[C.len_prefix_running:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:I=G
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_Y)
		if type(E)is web.Response:A=E;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(I,B);return A
		else:assert type(E)==str;H=E;assert H!=_K;J=utils.Encoding[H.rsplit(_G,1)[1]]
		if F==_A or F=='':A=web.Response(status=204)
		else:A=web.Response(status=404);A.content_type=H;J=utils.Encoding[A.content_type.rsplit(_G,1)[1]];K=utils.gen_rc_errors(_L,_Z,error_message=_AE);N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,N);B[_D]=K
		B[_F]=A.status;await C._insert_bootstrapping_log_entry(I,B);return A
	async def handle_post_config_request(C,request):
		D=request;F=D.path[C.len_prefix_running:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:J=G
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if type(E)is web.Response:A=E;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(J,B);return A
		else:assert type(E)==str;H=E;assert H!=_K;K=utils.Encoding[H.rsplit(_G,1)[1]]
		if F==_A or F=='':A=web.Response(status=400);I=utils.gen_rc_errors(_X,_a,error_message=_w)
		else:A=web.Response(status=404);I=utils.gen_rc_errors(_L,_Z,error_message=_x)
		A.content_type=H;K=utils.Encoding[A.content_type.rsplit(_G,1)[1]];N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,K,C.dm4errors,N);B[_F]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(J,B);return A
	async def handle_put_config_request(C,request):
		D=request;F=D.path[C.len_prefix_running:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:J=G
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if type(E)is web.Response:A=E;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(J,B);return A
		else:assert type(E)==str;H=E;assert H!=_K;K=utils.Encoding[H.rsplit(_G,1)[1]]
		if F==_A or F=='':A=web.Response(status=400);I=utils.gen_rc_errors(_X,_a,error_message=_w)
		else:A=web.Response(status=404);I=utils.gen_rc_errors(_L,_Z,error_message=_x)
		A.content_type=H;K=utils.Encoding[A.content_type.rsplit(_G,1)[1]];N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,K,C.dm4errors,N);B[_F]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(J,B);return A
	async def handle_delete_config_request(C,request):
		D=request;G=D.path[C.len_prefix_running:];H=await C._check_auth(D,G)
		if type(H)is web.Response:A=H;return A
		else:L=H
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;E,M=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if type(E)is web.Response:A=E;N=M;B[_F]=A.status;B[_D]=N;await C._insert_bootstrapping_log_entry(L,B);return A
		else:
			assert type(E)==str;I=E
			if I==_K:J=_C
			else:J=utils.Encoding[I.rsplit(_G,1)[1]]
		if G==_A or G=='':A=web.Response(status=400);F=_w;K=utils.gen_rc_errors(_X,_a,error_message=F)
		else:A=web.Response(status=404);F=_x;K=utils.gen_rc_errors(_L,_Z,error_message=F)
		A.content_type=I
		if J is _C:A.text=F
		else:O=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,O)
		B[_F]=A.status;B[_D]=K;await C._insert_bootstrapping_log_entry(L,B);return A
	async def handle_action_request(C,request):
		D=request;F=D.path[C.len_prefix_operational:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:J=G
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if type(E)is web.Response:A=E;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(J,B);return A
		else:assert type(E)==str;H=E;assert H!=_K;K=utils.Encoding[H.rsplit(_G,1)[1]]
		if F==_A or F=='':A=web.Response(status=400);I=utils.gen_rc_errors(_X,_a,error_message='Resource does not support action.')
		else:A=web.Response(status=404);I=utils.gen_rc_errors(_L,_Z,error_message=_AF)
		A.content_type=H;K=utils.Encoding[A.content_type.rsplit(_G,1)[1]];N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,K,C.dm4errors,N);B[_F]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(J,B);return A
	async def handle_rpc_request(C,request):
		M='sleep';D=request;F=D.path[C.len_prefix_operations:];J=await C._check_auth(D,F)
		if type(J)is web.Response:A=J;return A
		else:E=J
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=D.remote;B[_V]=D.method;B[_W]=D.path;H,N=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if type(H)is web.Response:A=H;O=N;B[_F]=A.status;B[_D]=O;await C._insert_bootstrapping_log_entry(E,B);return A
		else:
			assert type(H)==str;K=H
			if K==_K:L=_C
			else:L=utils.Encoding[K.rsplit(_G,1)[1]]
		if F==_y:
			async with C.nvh.fifolock(Read):
				if os.environ.get('SZTPD_INIT_MODE')and M in D.query:await asyncio.sleep(int(D.query[M]))
				A=await C._handle_get_bootstrapping_data_rpc(E,D,B);B[_F]=A.status;await C._insert_bootstrapping_log_entry(E,B);return A
		elif F==_AG:
			try:A=await C._handle_report_progress_rpc(E,D,B)
			except NotImplementedError as Q:raise NotImplementedError('is this ever called?')
			B[_F]=A.status;await C._insert_bootstrapping_log_entry(E,B);return A
		elif F==_A or F=='':A=web.Response(status=400);G=_AF;I=utils.gen_rc_errors(_X,_a,error_message=G)
		else:A=web.Response(status=404);G='Unrecognized RPC.';I=utils.gen_rc_errors(_L,_Z,error_message=G)
		A.content_type=K
		if A.content_type==_K:A.text=G
		else:I=utils.gen_rc_errors(_L,_a,error_message=G);P=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,L,C.dm4errors,P)
		B[_F]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(E,B);return A
	async def _check_auth(A,request,data_path):
		m='num-times-accessed';l='local-truststore-reference';k=':device-type';j='identity-certificates';i='activation-code';h='" not found for any tenant.';g='Device "';f='X-Client-Cert';V='verification';U='device-type';Q='sbi-access-stats';M='lifecycle-statistics';J='comment';I='failure';F='outcome';C=request
		def G(request,supported_media_types):
			E=supported_media_types;D='Accept';C=request;B=web.Response(status=401)
			if D in C.headers and any((C.headers[D]==A for A in E)):B.content_type=C.headers[D]
			elif _h in C.headers and any((C.headers[_h]==A for A in E)):B.content_type=C.headers[_h]
			else:B.content_type=_K
			if B.content_type!=_K:F=utils.Encoding[B.content_type.rsplit(_G,1)[1]];G=utils.gen_rc_errors(_L,_z);H=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(G,F,A.dm4errors,H)
			return B
		B={};B[_T]=datetime.datetime.utcnow();B[_U]=C.remote;B['source-proxies']=list(C.forwarded);B['host']=C.host;B[_V]=C.method;B[_W]=C.path;K=set();N=_C;O=C.transport.get_extra_info('peercert')
		if O is not _C:P=O['subject'][-1][0][1];K.add(P)
		elif C.headers.get(f)!=_C:n=C.headers.get(f);W=bytes(urllib.parse.unquote(n),'utf-8');N=x509.load_pem_x509_certificate(W,default_backend());o=N.subject;P=o.get_attributes_for_oid(x509.ObjectIdentifier('2.5.4.5'))[0].value;K.add(P)
		R=_C;X=_C;S=C.headers.get('AUTHORIZATION')
		if S!=_C:R,X=basicauth.decode(S);K.add(R)
		if len(K)==0:B[F]=I;B[J]='Device provided no identification credentials.';await A._insert_audit_log_entry(_C,B);return G(C,A.supported_media_types)
		if len(K)!=1:B[F]=I;B[J]='Device provided mismatched authentication credentials ('+P+' != '+R+').';await A._insert_audit_log_entry(_C,B);return G(C,A.supported_media_types)
		E=K.pop();D=_C
		if A.mode==_S:L=_A+A.dal.app_ns+_i
		elif A.mode=='1':L=_A+A.dal.app_ns+_AB+E
		if A.mode!='x':
			try:D=await A.dal.handle_get_opstate_request(L)
			except dal.NodeNotFound as Y:B[F]=I;B[J]=g+E+h;await A._insert_audit_log_entry(_C,B);return G(C,A.supported_media_types)
			H=_C
		else:
			try:H=await A.dal.get_tenant_name_for_global_key(_A+A.dal.app_ns+':tenants/tenant/devices/device',E)
			except dal.NodeNotFound as Y:B[F]=I;B[J]=g+E+h;await A._insert_audit_log_entry(_C,B);return G(C,A.supported_media_types)
			L=_A+A.dal.app_ns+_e+H+_AC+E;D=await A.dal.handle_get_opstate_request(L)
		assert D!=_C;assert A.dal.app_ns+_i in D;D=D[A.dal.app_ns+_i]
		if A.mode!=_S:D=D[0]
		if i in D:
			if S==_C:B[F]=I;B[J]='Activation code required but none passed for serial number '+E;await A._insert_audit_log_entry(H,B);return G(C,A.supported_media_types)
			Z=D[i];assert Z.startswith('$5$')
			if not sha256_crypt.verify(X,Z):B[F]=I;B[J]='Activation code mismatch for serial number '+E;await A._insert_audit_log_entry(H,B);return G(C,A.supported_media_types)
		else:0
		assert U in D;p=_A+A.dal.app_ns+':device-types/device-type='+D[U];a=await A.dal.handle_get_opstate_request(p)
		if j in a[A.dal.app_ns+k][0]:
			if O is _C and N is _C:B[F]=I;B[J]='Client cert required but none passed for serial number '+E;await A._insert_audit_log_entry(H,B);return G(C,A.supported_media_types)
			if O:b=C.transport.get_extra_info(_A0);assert b is not _C;c=b.getpeercert(_Y)
			else:assert N is not _C;c=W
			T=a[A.dal.app_ns+k][0][j];assert V in T;assert l in T[V];d=T[V][l];q=_A+A.dal.app_ns+':truststore/certificate-bags/certificate-bag='+d['certificate-bag']+'/certificate='+d['certificate'];r=await A.dal.handle_get_config_request(q);s=r[A.dal.app_ns+':certificate'][0]['cert-data'];t=base64.b64decode(s);u,v=der_decoder(t,asn1Spec=rfc5652.ContentInfo());assert not v;w=utils.degenerate_cms_obj_to_ders(u);x=ValidationContext(trust_roots=w);y=CertificateValidator(c,validation_context=x)
			try:y._validate_path()
			except PathBuildingError as Y:B[F]=I;B[J]="Client cert for serial number '"+E+"' does not validate using trust anchors specified by device-type '"+D[U]+"'";await A._insert_audit_log_entry(H,B);return G(C,A.supported_media_types)
		B[F]='success';await A._insert_audit_log_entry(H,B);z=L+'/lifecycle-statistics';e=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
		if D[M][Q][m]==0:D[M][Q]['first-accessed']=e
		D[M][Q]['last-accessed']=e;D[M][Q][m]+=1;await A.dal.handle_put_opstate_request(z,D[M]);return E,H
	async def _handle_get_bootstrapping_data_rpc(A,device_id,request,bootstrapping_log_entry):
		AQ='ietf-sztp-bootstrap-server:output';AP='content';AO='contentType';AN=':configuration';AM='configuration-handling';AL='script';AK='hash-value';AJ='hash-algorithm';AI='address';AH='referenced-definition';AG='match-criteria';AF='matched-response';A6='post-configuration-script';A5='configuration';A4='pre-configuration-script';A3='os-version';A2='os-name';A1='trust-anchor';A0='port';z='bootstrap-server';y='ietf-sztp-conveyed-info:redirect-information';x='value';w='response-manager';p=device_id;o='image-verification';n='download-uri';m='boot-image';l='selected-response';h='onboarding-information';g='key';d='reference';Z=request;Y='ietf-sztp-conveyed-info:onboarding-information';X='redirect-information';L='response';J='managed-response';I='response-details';E='get-bootstrapping-data-event';D='conveyed-information';C=bootstrapping_log_entry;i,AR=utils.check_http_headers(Z,A.supported_media_types,accept_required=_Y)
		if type(i)is web.Response:B=i;AS=AR;C[_F]=B.status;C[_D]=AS;return B
		else:assert type(i)==str;O=i;assert O!=_K;T=utils.Encoding[O.rsplit(_G,1)[1]]
		M=_C
		if Z.body_exists:
			AT=await Z.text();AU=utils.Encoding[Z.headers[_h].rsplit(_G,1)[1]]
			try:G=A.dm.get_schema_node(_y);M=utils.encoded_str_to_obj(AT,AU,A.dm,G)
			except Exception as a:B=web.Response(status=400);q=_m+str(a);B.content_type=O;H=utils.gen_rc_errors(_L,_g,error_message=q);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,T,A.dm4errors,G);C[_D]=H;return B
			if not _O in M:
				B=web.Response(status=400)
				if not _O in M:q=_m+_AH
				B.content_type=O;H=utils.gen_rc_errors(_L,_g,error_message=q);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,T,A.dm4errors,G);C[_D]=H;return B
		C[_B]={};C[_B][E]={}
		if M is _C:C[_B][E][_A1]={'no-input-passed':[_C]}
		else:C[_B][E][_A1]=M[_O]
		if A.mode!='x':P=_A+A.dal.app_ns+':'
		else:P=_A+A.dal.app_ns+_e+p[1]+_A
		if A.mode==_S:A7=P+'device'
		else:A7=P+'devices/device='+p[0]
		try:R=await A.dal.handle_get_config_request(A7)
		except Exception as a:B=web.Response(status=501);B.content_type=_k;H=utils.gen_rc_errors(_X,_j,error_message='Unhandled exception: '+str(a));B.text=utils.enc_rc_errors('json',H);return B
		assert R!=_C;assert A.dal.app_ns+_i in R;R=R[A.dal.app_ns+_i]
		if A.mode!=_S:R=R[0]
		if w not in R or AF not in R[w]:B=web.Response(status=404);B.content_type=O;H=utils.gen_rc_errors(_X,_n,error_message='No responses configured.');G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,T,A.dm4errors,G);C[_D]=H;C[_B][E][l]='no-responses-configured';return B
		F=_C
		for j in R[w][AF]:
			if not AG in j:F=j;break
			if M is _C:continue
			for Q in j[AG]['match']:
				if Q[g]not in M[_O]:break
				if'present'in Q:
					if'not'in Q:
						if Q[g]in M[_O]:break
					elif Q[g]not in M[_O]:break
				elif x in Q:
					if'not'in Q:
						if Q[x]==M[_O][Q[g]]:break
					elif Q[x]!=M[_O][Q[g]]:break
				else:raise NotImplementedError("Unrecognized 'match' expression.")
			else:F=j;break
		if F is _C or'none'in F[L]:
			if F is _C:C[_B][E][l]='no-match-found'
			else:C[_B][E][l]=F[_I]+" (explicit 'none')"
			B=web.Response(status=404);B.content_type=O;H=utils.gen_rc_errors(_X,_n,error_message='No matching responses configured.');G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,T,A.dm4errors,G);C[_D]=H;return B
		C[_B][E][l]=F[_I];C[_B][E][I]={J:{}}
		if D in F[L]:
			C[_B][E][I][J]={D:{}};N={}
			if _E in F[L][D]:
				C[_B][E][I][J][D]={_E:{}};assert d in F[L][D][_E];r=F[L][D][_E][d];C[_B][E][I][J][D][_E][_I]=r;S=await A.dal.handle_get_config_request(P+'dynamic-callouts/dynamic-callout='+r);assert r==S[A.dal.app_ns+_H][0][_I];C[_B][E][I][J][D][_E][_o]=S[A.dal.app_ns+_H][0][_o];b={}
				if A.mode!=_S:b[_p]=p[0]
				else:b[_p]=_AI
				b[_AJ]=Z.remote;A8=Z.transport.get_extra_info(_A0)
				if A8:
					A9=A8.getpeercert(_Y)
					if A9:b[_AK]=A9
				if M:b[_AL]=M
				if _b in S[A.dal.app_ns+_H][0]:
					C[_B][E][I][J][D][_E][_A2]=_b;AA=S[A.dal.app_ns+_H][0][_b][_q];AB=S[A.dal.app_ns+_H][0][_b][_r];C[_B][E][I][J][D][_E][_AM]={_q:AA,_r:AB};C[_B][E][I][J][D][_E][_c]={}
					if _s in S[A.dal.app_ns+_H][0]:AC=S[A.dal.app_ns+_H][0][_s]
					else:AC=_C
					K=_C
					try:K=A.nvh.plugins[AA][_AN][AB](b,AC)
					except Exception as a:C[_B][E][I][J][D][_E][_c][_AO]=str(a);B=web.Response(status=500);B.content_type=O;H=utils.gen_rc_errors(_X,_j,error_message='Server encountered an error while trying to generate a response: '+str(a));G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,T,A.dm4errors,G);C[_D]=H;return B
					assert K and type(K)==dict
					if _J in K:
						assert len(K[_J][_M])==1
						if any((A==K[_J][_M][0][_N]for A in(_a,'too-big',_AP,_AQ,_AR,_AS,_Z,_AT,_g))):B=web.Response(status=400)
						elif any((A==K[_J][_M][0][_N]for A in _z)):B=web.Response(status=403)
						elif any((A==K[_J][_M][0][_N]for A in('in-use',_AU,_AV,_AW,_n))):B=web.Response(status=409)
						elif any((A==K[_J][_M][0][_N]for A in(_AX,_AY,_AZ))):B=web.Response(status=500)
						elif any((A==K[_J][_M][0][_N]for A in _j)):B=web.Response(status=501)
						else:raise NotImplementedError(_Aa+K[_J][_M][0][_N])
						B.content_type=O;H=K;G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,T,A.dm4errors,G);C[_D]=K;C[_B][E][I][J][D][_E][_c][_t]=_Ab;return B
					else:C[_B][E][I][J][D][_E][_c][_t]='Returning conveyed information provided by callback.'
				elif _A3 in S[A.dal.app_ns+_H][0]:C[_B][E][I][J][D][_E][_A2]=_u;raise NotImplementedError('webhooks callout support pending!')
				else:raise NotImplementedError('unhandled dynamic callout type: '+str(S[A.dal.app_ns+_H][0]))
				N=K
			elif X in F[L][D]:
				C[_B][E][I][J][D]={X:{}};N[y]={};N[y][z]=[]
				if d in F[L][D][X]:
					e=F[L][D][X][d];C[_B][E][I][J][D][X]={AH:e};s=await A.dal.handle_get_config_request(P+'conveyed-information-responses/redirect-information-response='+e)
					for AV in s[A.dal.app_ns+':redirect-information-response'][0][X][z]:
						W=await A.dal.handle_get_config_request(P+'bootstrap-servers/bootstrap-server='+AV);W=W[A.dal.app_ns+':bootstrap-server'][0];k={};k[AI]=W[AI]
						if A0 in W:k[A0]=W[A0]
						if A1 in W:k[A1]=W[A1]
						N[y][z].append(k)
				else:raise NotImplementedError('unhandled redirect-information config type: '+str(F[L][D][X]))
			elif h in F[L][D]:
				C[_B][E][I][J][D]={};N[Y]={}
				if d in F[L][D][h]:
					e=F[L][D][h][d];C[_B][E][I][J][D][h]={AH:e};s=await A.dal.handle_get_config_request(P+'conveyed-information-responses/onboarding-information-response='+e);U=s[A.dal.app_ns+':onboarding-information-response'][0][h]
					if m in U:
						AW=U[m];AX=await A.dal.handle_get_config_request(P+'boot-images/boot-image='+AW);V=AX[A.dal.app_ns+':boot-image'][0];N[Y][m]={};c=N[Y][m]
						if A2 in V:c[A2]=V[A2]
						if A3 in V:c[A3]=V[A3]
						if n in V:
							c[n]=list()
							for AY in V[n]:c[n].append(AY)
						if o in V:
							c[o]=list()
							for AD in V[o]:t={};t[AJ]=AD[AJ];t[AK]=AD[AK];c[o].append(t)
					if A4 in U:AZ=U[A4];Aa=await A.dal.handle_get_config_request(P+'scripts/pre-configuration-script='+AZ);N[Y][A4]=Aa[A.dal.app_ns+':pre-configuration-script'][0][AL]
					if A5 in U:Ab=U[A5];AE=await A.dal.handle_get_config_request(P+'configurations/configuration='+Ab);N[Y][AM]=AE[A.dal.app_ns+AN][0][AM];N[Y][A5]=AE[A.dal.app_ns+AN][0]['config']
					if A6 in U:Ac=U[A6];Ad=await A.dal.handle_get_config_request(P+'scripts/post-configuration-script='+Ac);N[Y][A6]=Ad[A.dal.app_ns+':post-configuration-script'][0][AL]
			else:raise NotImplementedError('unhandled conveyed-information type: '+str(F[L][D]))
		else:raise NotImplementedError('unhandled response type: '+str(F[L]))
		f=rfc5652.ContentInfo()
		if O==_k:f[AO]=A.id_ct_sztpConveyedInfoJSON;f[AP]=encode_der(json.dumps(N,indent=2),asn1Spec=univ.OctetString())
		else:assert O==_A4;f[AO]=A.id_ct_sztpConveyedInfoXML;G=A.dm4conveyedinfo.get_schema_node(_A);assert G;Ae=utils.obj_to_encoded_str(N,T,A.dm4conveyedinfo,G,strip_wrapper=_Y);f[AP]=encode_der(Ae,asn1Spec=univ.OctetString())
		Af=encode_der(f,rfc5652.ContentInfo());u=base64.b64encode(Af).decode('ASCII');Ag=base64.b64decode(u);Ah=base64.b64encode(Ag).decode('ASCII');assert u==Ah;v={};v[AQ]={};v[AQ][D]=u;B=web.Response(status=200);B.content_type=O;G=A.dm.get_schema_node(_y);B.text=utils.obj_to_encoded_str(v,T,A.dm,G);return B
	async def _handle_report_progress_rpc(A,device_id,request,bootstrapping_log_entry):
		g='remote-port';f='webhook-results';Y='tcp-client-parameters';X='encoding';W=device_id;V='http';L=request;E='report-progress-event';C=bootstrapping_log_entry;S,h=utils.check_http_headers(L,A.supported_media_types,accept_required=_f)
		if type(S)is web.Response:B=S;i=h;C[_F]=B.status;C[_D]=i;return B
		else:assert type(S)==str;J=S
		if J!=_K:O=utils.Encoding[J.rsplit(_G,1)[1]]
		if not L.body_exists:
			M='RPC "input" node missing (required for "report-progress").';B=web.Response(status=400);B.content_type=J
			if B.content_type==_K:B.text=M
			else:F=utils.gen_rc_errors(_L,_a,error_message=M);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(F,O,A.dm4errors,G)
			C[_D]=B.text;return B
		j=utils.Encoding[L.headers[_h].rsplit(_G,1)[1]];k=await L.text()
		try:G=A.dm.get_schema_node(_AG);P=utils.encoded_str_to_obj(k,j,A.dm,G)
		except Exception as K:B=web.Response(status=400);M=_m+str(K);B.content_type=J;F=utils.gen_rc_errors(_L,_g,error_message=M);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(F,O,A.dm4errors,G);C[_D]=F;return B
		if not _O in P:
			B=web.Response(status=400)
			if not _O in P:M=_m+_AH
			B.content_type=J;F=utils.gen_rc_errors(_L,_g,error_message=M);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(F,O,A.dm4errors,G);C[_D]=F;return B
		C[_B]={};C[_B][E]={};C[_B][E][_A1]=P[_O];C[_B][E][_E]={}
		if A.mode==_S or A.mode=='1':Q=_A+A.dal.app_ns+':preferences/outbound-interactions/relay-progress-report-callout'
		elif A.mode=='x':Q=_A+A.dal.app_ns+_e+W[1]+'/preferences/outbound-interactions/relay-progress-report-callout'
		try:l=await A.dal.handle_get_config_request(Q)
		except Exception as K:C[_B][E][_E]['no-callout-configured']=[_C]
		else:
			T=l[A.dal.app_ns+':relay-progress-report-callout'];C[_B][E][_E][_I]=T
			if A.mode==_S or A.mode=='1':Q=_A+A.dal.app_ns+':dynamic-callouts/dynamic-callout='+T
			elif A.mode=='x':Q=_A+A.dal.app_ns+_e+W[1]+'/dynamic-callouts/dynamic-callout='+T
			H=await A.dal.handle_get_config_request(Q);assert T==H[A.dal.app_ns+_H][0][_I];C[_B][E][_E][_o]=H[A.dal.app_ns+_H][0][_o];N={}
			if A.mode!=_S:N[_p]=W[0]
			else:N[_p]=_AI
			N[_AJ]=L.remote;Z=L.transport.get_extra_info(_A0)
			if Z:
				a=Z.getpeercert(_Y)
				if a:N[_AK]=a
			if P:N[_AL]=P
			if _b in H[A.dal.app_ns+_H][0]:
				C[_B][E][_E][_A2]=_b;b=H[A.dal.app_ns+_H][0][_b][_q];c=H[A.dal.app_ns+_H][0][_b][_r];C[_B][E][_E][_AM]={_q:b,_r:c};C[_B][E][_E][_c]={}
				if _s in H[A.dal.app_ns+_H][0]:d=H[A.dal.app_ns+_H][0][_s]
				else:d=_C
				D=_C
				try:D=A.nvh.plugins[b][_AN][c](N,d)
				except Exception as K:C[_B][E][_E][_c][_AO]=str(K);B=web.Response(status=500);B.content_type=J;F=utils.gen_rc_errors(_X,_j,error_message='Server encountered an error while trying to process the progress report: '+str(K));G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(F,O,A.dm4errors,G);C[_D]=F;return B
				if D:
					assert type(D)==dict;assert len(D)==1;assert _J in D;assert len(D[_J][_M])==1
					if any((A==D[_J][_M][0][_N]for A in(_a,'too-big',_AP,_AQ,_AR,_AS,_Z,_AT,_g))):B=web.Response(status=400)
					elif any((A==D[_J][_M][0][_N]for A in _z)):B=web.Response(status=403)
					elif any((A==D[_J][_M][0][_N]for A in('in-use',_AU,_AV,_AW,_n))):B=web.Response(status=409)
					elif any((A==D[_J][_M][0][_N]for A in(_AX,_AY,_AZ))):B=web.Response(status=500)
					elif any((A==D[_J][_M][0][_N]for A in _j)):B=web.Response(status=501)
					else:raise NotImplementedError(_Aa+D[_J][_M][0][_N])
					B.content_type=J;F=D;G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(F,O,A.dm4errors,G);C[_D]=D;C[_B][E][_E][_c][_t]=_Ab;return B
				else:C[_B][E][_E][_c][_t]='Callback returned no output (normal)'
			elif _A3 in H[A.dal.app_ns+_H][0]:
				C[_B][E][_E][f]={_u:[]}
				for I in H[A.dal.app_ns+_H][0][_A3][_u]:
					R={};R[_I]=I[_I]
					if X not in I or I[X]=='json':e=rpc_input_json
					elif I[X]=='xml':e=rpc_input_xml
					if V in I:
						U='http://'+I[V][Y]['remote-address']
						if g in I[V][Y]:U+=':'+str(I[V][Y][g])
						U+='/relay-notification';R['uri']=U
						try:
							async with aiohttp.ClientSession()as m:B=await m.post(U,data=e)
						except aiohttp.client_exceptions.ClientConnectorError as K:R['connection-error']=str(K)
						else:
							R['http-status-code']=B.status
							if B.status==200:break
					else:assert'https'in I;raise NotImplementedError('https-based webhook is not supported yet.')
					C[_B][E][_E][f][_u].append(R)
			else:raise NotImplementedError('unrecognized callout type '+str(H[A.dal.app_ns+_H][0]))
		B=web.Response(status=204);return B