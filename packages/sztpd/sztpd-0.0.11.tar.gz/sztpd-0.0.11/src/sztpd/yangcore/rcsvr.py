# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_C='/ds/ietf-datastores:operational'
_B='/ds/ietf-datastores:running'
_A=None
import os,ssl,json,base64,pyasn1,asyncio,yangson,datetime,tempfile,basicauth
from .  import utils
from aiohttp import web
from .handler import RouteHandler
from pyasn1.type import univ
from pyasn1_modules import rfc3447
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5915
from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder
async def set_server_header(request,response):response.headers['Server']='<redacted>'
class RestconfServer:
	root='/restconf';prefix_running=root+_B;prefix_operational=root+_C;prefix_operations=root+'/operations';len_prefix_running=len(prefix_running);len_prefix_operational=len(prefix_operational);len_prefix_operations=len(prefix_operations)
	def __init__(A,loop,dal,endpoint_config,view_handler,facade_yl=_A):
		w='client-certs';v='local-truststore-reference';u='ca-certs';t='client-authentication';s='\n-----END CERTIFICATE-----\n';r='-----BEGIN CERTIFICATE-----\n';q='cert-data';p='private-key-format';o=':keystore/asymmetric-keys/asymmetric-key=';n='reference';m='server-identity';l='local-port';k='http';V='ASCII';U=':asymmetric-key';T='tcp-server-parameters';M='certificate';L='tls-server-parameters';K='/ds/ietf-datastores:running{tail:.*}';J='/';G=dal;D='https';C=endpoint_config;B=view_handler;A.len_prefix_running=len(A.root+_B);A.len_prefix_operational=len(A.root+_C);A.loop=loop;A.dal=G;A.name=C['name'];A.view_handler=B;A.app=web.Application(client_max_size=1024*1024*32);A.app.on_response_prepare.append(set_server_header);A.app.router.add_get('/.well-known/host-meta',A.handle_get_host_meta);A.app.router.add_get(A.root,B.handle_get_restconf_root);A.app.router.add_get(A.root+J,B.handle_get_restconf_root);A.app.router.add_get(A.root+'/yang-library-version',B.handle_get_yang_library_version);A.app.router.add_get(A.root+'/ds/ietf-datastores:operational{tail:.*}',B.handle_get_opstate_request);A.app.router.add_get(A.root+K,B.handle_get_config_request);A.app.router.add_put(A.root+K,B.handle_put_config_request);A.app.router.add_post(A.root+K,B.handle_post_config_request);A.app.router.add_delete(A.root+K,B.handle_delete_config_request);A.app.router.add_post(A.root+'/ds/ietf-datastores:operational/{tail:.*}',B.handle_action_request);A.app.router.add_post(A.root+'/operations/{tail:.*}',B.handle_rpc_request)
		if k in C:F=k
		else:assert D in C;F=D
		A.local_address=C[F][T]['local-address'];A.local_port=os.environ.get('SZTPD_INIT_PORT',8080)
		if l in C[F][T]:A.local_port=C[F][T][l]
		E=_A
		if F==D:
			W=C[D][L][m][M][n]['asymmetric-key'];N=A.dal.handle_get_config_request(J+A.dal.app_ns+o+W);O=A.loop.run_until_complete(N);P=O[A.dal.app_ns+U][0]['cleartext-private-key'];X=base64.b64decode(P)
			if O[A.dal.app_ns+U][0][p]=='ietf-crypto-types:ec-private-key-format':Q,x=der_decoder(X,asn1Spec=rfc5915.ECPrivateKey());y=der_encoder(Q);Y=base64.b64encode(y).decode(V);assert P==Y;Z='-----BEGIN EC PRIVATE KEY-----\n'+Y+'\n-----END EC PRIVATE KEY-----\n'
			elif O[A.dal.app_ns+U][0][p]=='ietf-crypto-types:rsa-private-key-format':Q,x=der_decoder(X,asn1Spec=rfc3447.RSAPrivateKey());z=der_encoder(Q);a=base64.b64encode(z).decode(V);assert P==a;Z='-----BEGIN RSA PRIVATE KEY-----\n'+a+'\n-----END RSA PRIVATE KEY-----\n'
			else:raise NotImplementedError('this line can never be reached')
			A0=C[D][L][m][M][n][M];N=A.dal.handle_get_config_request(J+A.dal.app_ns+o+W+'/certificates/certificate='+A0);A1=A.loop.run_until_complete(N);A2=A1[A.dal.app_ns+':certificate'][0][q];A3=base64.b64decode(A2);A4,b=der_decoder(A3,asn1Spec=rfc5652.ContentInfo());A5=A4.getComponentByName('content');A6,b=der_decoder(A5,asn1Spec=rfc5652.SignedData());c=A6.getComponentByName('certificates');H=''
			for A7 in range(len(c)):
				d=c[A7][0]
				for e in d['tbsCertificate']['extensions']:
					if e['extnID']==rfc5280.id_ce_basicConstraints:A8,b=der_decoder(e['extnValue'],asn1Spec=rfc5280.BasicConstraints())
				A9=der_encoder(d);f=base64.b64encode(A9).decode(V)
				if A8['cA']==False:H=r+f+s+H
				else:H+=r+f+s
			E=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH);E.verify_mode=ssl.CERT_OPTIONAL
			with tempfile.TemporaryDirectory()as g:
				h=g+'key.pem';i=g+'certs.pem'
				with open(h,'w')as AA:AA.write(Z)
				with open(i,'w')as AB:AB.write(H)
				E.load_cert_chain(i,h)
			if t in C[D][L]:
				I=C[D][L][t]
				def j(truststore_ref):
					C=G.handle_get_config_request(J+G.app_ns+':truststore/certificate-bags/certificate-bag='+truststore_ref);D=A.loop.run_until_complete(C);B=[]
					for E in D[G.app_ns+':certificate-bag'][0][M]:F=base64.b64decode(E[q]);H,I=der_decoder(F,asn1Spec=rfc5652.ContentInfo());assert not I;B+=utils.degenerate_cms_obj_to_ders(H)
					return B
				R=[]
				if u in I:S=I[u][v];R+=j(S)
				if w in I:S=I[w][v];R+=j(S)
				AC=utils.der_dict_to_multipart_pem({'CERTIFICATE':R});E.load_verify_locations(cadata=AC)
		if F==D:assert not E is _A
		else:assert E is _A
		A.runner=web.AppRunner(A.app);A.loop.run_until_complete(A.runner.setup());A.site=web.TCPSite(A.runner,host=A.local_address,port=A.local_port,ssl_context=E,reuse_port=True);A.loop.run_until_complete(A.site.start())
	async def handle_get_host_meta(B,request):A=web.Response();A.content_type='application/xrd+xml';A.text='<XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">\n  <Link rel="restconf" href="/restconf"/>\n</XRD>';return A