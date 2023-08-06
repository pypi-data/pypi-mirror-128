# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

_F='tested?'
_E='wn-sztpd-0:device'
_D='device'
_C='activation-code'
_B='/'
_A=None
import gc,tracemalloc,os,re,json,base64,signal,asyncio,datetime,functools,pkg_resources
from passlib.hash import sha256_crypt
from .yangcore import utils
from .yangcore.rcsvr import RestconfServer
from .yangcore.tenant import TenantViewHandler
from .yangcore.native import NativeViewHandler,Period,TimeUnit
from .yangcore.dal import DataAccessLayer,CreateCallbackFailed,CreateOrChangeCallbackFailed,ChangeCallbackFailed,AuthenticationFailed
from .rfc8572 import RFC8572ViewHandler
from .  import yl
from pyasn1.codec.der.decoder import decode as decode_der
from pyasn1.error import PyAsn1Error
from pyasn1_modules import rfc5652
from cryptography import x509
from cryptography.hazmat.primitives import serialization
loop=_A
sig=_A
def signal_handler(name):global loop;global sig;sig=name;loop.stop()
def run(db_url,cacert_param=_A,cert_param=_A,key_param=_A):
	b=':tenants/tenant/bootstrap-servers/bootstrap-server/trust-anchor';a=':bootstrap-servers/bootstrap-server/trust-anchor';Z=':transport';Y='SIGHUP';X='Yes';S='use-for';R='1';O=db_url;N='x';L=key_param;K=cert_param;J=cacert_param;global loop;global sig;A=_A;B=_A;T=False
	if J is not _A and O.startswith('sqlite:'):print('The "sqlite" dialect does not support the "cacert" parameter.');return 1
	if(K or L)and not J:print('The "cacert" parameter must be specified whenever the "key" and "cert" parameters are specified.');return 1
	if(K is _A)!=(L is _A):print('The "key" and "cert" parameters must be specified together.');return 1
	try:A=DataAccessLayer(O,J,K,L)
	except (SyntaxError,AssertionError,AuthenticationFailed)as H:print(str(H));return 1
	except NotImplementedError as H:T=True
	else:B=A.opaque()
	if T==True:
		D=os.environ.get('SZTPD_ACCEPT_CONTRACT')
		if D==_A:
			print('');c=pkg_resources.resource_filename('sztpd','LICENSE.txt');U=open(c,'r');print(U.read());U.close();print('First time initialization.  Please accept the license terms.');print('');print('By entering "Yes" below, you agree to be bound to the terms and conditions contained on this screen with Watsen Networks.');print('');d=input('Please enter "Yes" or "No": ')
			if d!=X:print('');print('Thank you for your consideration.');print('');return 1
		elif D!=X:print('');print('The "SZTPD_ACCEPT_CONTRACT" environment variable is set to a value other than "Yes".  Please correct the value and try again.');print('');return 1
		D=os.environ.get('SZTPD_INIT_MODE')
		if D==_A:
			print('');print('Modes:');print('  1 - single-tenant');print('  x - multi-tenant');print('');B=input('Please select mode: ')
			if B not in[R,N]:print('Unknown mode selection.  Please try again.');return 1
			print('');print("Running SZTPD in mode '"+B+"'. (No more output expected)");print('')
		elif D not in[R,N]:print('The "SZTPD_INIT_MODE" environment variable is set to an unknown value.  Must be \'1\' or \'x\'.');return 1
		else:B=D
		D=os.environ.get('SZTPD_INIT_PORT')
		if D!=_A:
			try:V=int(D)
			except ValueError as H:print('Invalid "SZTPD_INIT_PORT" value ('+D+').');return 1
			if V<=0 or V>2**16-1:print('The "SZTPD_INIT_PORT" value ('+D+') is out of range [1..65535].');return 1
		try:A=DataAccessLayer(O,J,K,L,json.loads(getattr(yl,'nbi_'+B)()),'wn-sztpd-'+B,B)
		except Exception as H:raise H;return 1
	assert B!=_A;assert A!=_A;tracemalloc.start(25);loop=asyncio.get_event_loop();loop.add_signal_handler(signal.SIGHUP,functools.partial(signal_handler,name=Y));loop.add_signal_handler(signal.SIGTERM,functools.partial(signal_handler,name='SIGTERM'));loop.add_signal_handler(signal.SIGINT,functools.partial(signal_handler,name='SIGINT'));loop.add_signal_handler(signal.SIGQUIT,functools.partial(signal_handler,name='SIGQUIT'))
	while sig is _A:
		M=[];F=A.handle_get_config_request(_B+A.app_ns+Z);P=loop.run_until_complete(F)
		for E in P[A.app_ns+Z]['listen']['endpoint']:
			if E[S]=='native-interface':
				C=NativeViewHandler(A,B,loop)
				if B=='0':G=_B+A.app_ns+':device'
				elif B==R:G=_B+A.app_ns+':devices/device'
				elif B==N:G=_B+A.app_ns+':tenants/tenant/devices/device'
				C.register_create_callback(G,_handle_device_created);e=G+'/activation-code';C.register_change_callback(e,_handle_device_act_code_changed);C.register_subtree_change_callback(G,_handle_device_subtree_changed);C.register_somehow_change_callback(G,_handle_device_somehow_changed);C.register_delete_callback(G,_handle_device_deleted);C.register_periodic_callback(Period(24,TimeUnit.Hours),datetime.datetime(2000,1,1,0),_check_expirations)
				if B!=N:C.register_create_callback(_B+A.app_ns+a,_handle_bss_trust_anchor_cert_created_or_changed);C.register_change_callback(_B+A.app_ns+a,_handle_bss_trust_anchor_cert_created_or_changed)
				else:C.register_create_callback(_B+A.app_ns+b,_handle_bss_trust_anchor_cert_created_or_changed);C.register_change_callback(_B+A.app_ns+b,_handle_bss_trust_anchor_cert_created_or_changed)
				Q=RestconfServer(loop,A,E,C)
			elif E[S]=='tenant-interface':
				def f():return getattr(yl,'nbi_x_tenant')()
				g=TenantViewHandler(C,f);Q=RestconfServer(loop,A,E,g)
			else:assert E[S]=='rfc8572-interface';W=json.loads(getattr(yl,'sbi_rfc8572')());h=RFC8572ViewHandler(A,B,W,C);Q=RestconfServer(loop,A,E,h,W)
			M.append(Q);del E;E=_A
		del P;P=_A;loop.run_forever()
		for I in M:F=I.app.shutdown();loop.run_until_complete(F);F=I.runner.cleanup();loop.run_until_complete(F);F=I.app.cleanup();loop.run_until_complete(F);del I;I=_A
		del M;M=_A
		if sig==Y:sig=_A
	loop.close();del A;return 0
async def _handle_device_created_post_sweep(watched_node_path,conn,opaque):
	g=':dynamic-callout';f='webhooks';e='verification-result';d='failure';c='tenant';b='function';a='functions';Z='plugin';Y='callback';X='ownership-authorization';O='verification-results';N='dynamic-callout';M='device-type';L='row_id';K='=[^/]*';I=watched_node_path;H='wn-sztpd-rpcs:output';B=conn;A=opaque;C=A.dal._get_row_data_for_list_path(I,B);D=re.sub(K,'',I);h=A.dal._get_jsob_for_row_id_in_table(D,C[L],B);P=_B+A.dal.app_ns+':device-types/device-type='+h[_D][M];C=A.dal._get_row_data_for_list_path(P,B);D=re.sub(K,'',P);Q=A.dal._get_jsob_for_row_id_in_table(D,C[L],B)
	if X in Q[M]:
		R=_B+A.dal.app_ns+':dynamic-callouts/dynamic-callout='+Q[M][X][N]['reference'];C=A.dal._get_row_data_for_list_path(R,B);D=re.sub(K,'',R);E=A.dal._get_jsob_for_row_id_in_table(D,C[L],B)
		if Y in E[N]:
			F=E[N][Y];assert F[Z]in A.plugins;S=A.plugins[F[Z]];assert a in S;T=S[a];assert F[b]in T;i=T[F[b]];J=I.split(_B)
			if J[2]==c:U=J[1].split('=')[1]
			else:U='not-applicable'
			V=J[-1].split('=')[1];j={'wn-sztpd-rpcs:input':{c:U,'serial-number':[V]}};G=i(j);W=d
			if H in G:
				if O in G[H]:
					if e in G[H][O]:W=G[H][O][e][0]['result']
			if W==d:raise CreateCallbackFailed('Unable to verify ownership for device: '+V)
		else:assert f in E[A.dal.app_ns+g][0];k=E[A.dal.app_ns+g][0][f];raise NotImplementedError('webhooks for ownership verification not implemented yet')
async def _handle_device_created(watched_node_path,jsob,jsob_data_path,nvh):
	C=nvh;B=jsob;assert type(B)==dict
	if jsob_data_path==_B:assert _E in B;A=B[_E]
	else:assert _D in B;A=B[_D]
	if C.dal.post_dal_callbacks is _A:C.dal.post_dal_callbacks=[]
	C.dal.post_dal_callbacks.append((_handle_device_created_post_sweep,watched_node_path,C));A['lifecycle-statistics']={'nbi-access-stats':{'created':datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),'num-times-modified':0},'sbi-access-stats':{'num-times-accessed':0}};A['bootstrapping-log']={'log-entry':[]}
	if _C in A and A[_C].startswith('$0$'):A[_C]=sha256_crypt.using(rounds=1000).hash(A[_C][3:])
async def _handle_device_act_code_changed(watched_node_path,jsob,jsob_data_path,nvh):
	A=jsob;assert type(A)==dict
	if jsob_data_path==_B:assert _E in A;B=A[_E]
	else:assert _D in A;B=A[_D]
	if _C in B and B[_C].startswith('$0$'):B[_C]=sha256_crypt.using(rounds=1000).hash(B[_C][3:])
async def _handle_device_subtree_changed(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError(_F)
async def _handle_device_somehow_changed(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError(_F)
async def _handle_device_deleted(data_path,nvh):0
async def _handle_bss_trust_anchor_cert_created_or_changed(watched_node_path,jsob,jsob_data_path,obj):
	G='": ';B=watched_node_path;H=jsob['bootstrap-server']['trust-anchor'];I=base64.b64decode(H)
	try:J,O=decode_der(I,asn1Spec=rfc5652.ContentInfo())
	except PyAsn1Error as K:raise CreateOrChangeCallbackFailed('Parsing trust anchor certificate CMS structure failed for '+B+' ('+str(K)+')')
	L=utils.degenerate_cms_obj_to_ders(J);A=[]
	for M in L:N=x509.load_der_x509_certificate(M);A.append(N)
	D=[B for B in A if B.subject==B.issuer]
	if len(D)==0:raise CreateOrChangeCallbackFailed('Trust anchor certificates must encode a root (self-signed) certificate: '+B)
	if len(D)>1:raise CreateOrChangeCallbackFailed('Trust anchor certificates must encode no more than one root (self-signed) certificate ('+str(len(D))+' found): '+B)
	F=D[0];A.remove(F);C=F
	while len(A):
		E=[B for B in A if B.issuer==C.subject]
		if len(E)==0:raise CreateOrChangeCallbackFailed('Trust anchor certificates must not encode superfluous certificates.  CMS encodes additional certs not issued by the certificate "'+str(C.subject)+G+B)
		if len(E)>1:raise CreateOrChangeCallbackFailed('Trust anchor certificates must encode a single chain of certificates.  Found '+str(len(E))+' certificates issued by "'+str(C.subject)+G+B)
		C=E[0];A.remove(C)
def _check_expirations(nvh):0