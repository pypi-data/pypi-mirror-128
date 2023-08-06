# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

_P='content'
_O='certificates'
_N='certificate'
_M='2021-02-24'
_L='import'
_K='contentType'
_J='encoding = '
_I='utf-8'
_H='xml'
_G='json'
_F='implement'
_E='conformance-type'
_D='namespace'
_C='revision'
_B='name'
_A=None
import re,sys,pem,json,base64,yangson,datetime,textwrap,traceback,pkg_resources,xml.etree.ElementTree as ET
from enum import Enum
from aiohttp import web
from xml.dom import minidom
from pyasn1.type import tag
from urllib.parse import unquote
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5280
from pyasn1.codec.der import decoder as der_decoder
from pyasn1.codec.der import encoder as der_encoder
class RedundantQueryParameters(Exception):0
class MalformedDataPath(Exception):0
yl4errors={'ietf-yang-library:modules-state':{'module-set-id':'TBD','module':[{_B:'ietf-yang-types',_C:'2013-07-15',_D:'urn:ietf:params:xml:ns:yang:ietf-yang-types',_E:_L},{_B:'ietf-restconf',_C:'2017-01-26',_D:'urn:ietf:params:xml:ns:yang:ietf-restconf',_E:_F},{_B:'ietf-netconf-acm',_C:'2018-02-14',_D:'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',_E:_L},{_B:'ietf-sztp-bootstrap-server',_C:'2019-04-30',_D:'urn:ietf:params:xml:ns:yang:ietf-sztp-bootstrap-server',_E:_F},{_B:'ietf-yang-structure-ext',_C:'2020-06-22',_D:'urn:ietf:params:xml:ns:yang:ietf-yang-structure-ext',_E:_F},{_B:'ietf-sztp-csr',_C:_M,_D:'urn:ietf:params:xml:ns:yang:ietf-sztp-csr',_E:_F},{_B:'ietf-crypto-types',_C:_M,_D:'urn:ietf:params:xml:ns:yang:ietf-crypto-types',_E:_F}]}}
path=pkg_resources.resource_filename('sztpd','yang')
path4errors=pkg_resources.resource_filename('sztpd','yang4errors')
dm4errors=yangson.DataModel(json.dumps(yl4errors),[path4errors,path])
def gen_rc_errors(error_type,error_tag,error_app_tag=_A,error_path=_A,error_message=_A,error_info=_A):
	E=error_info;D=error_message;C=error_path;B=error_app_tag;A={};A['error-type']=error_type;A['error-tag']=error_tag
	if B is not _A:A['error-app-tag']=B
	if C is not _A:A['error-path']=C
	if D is not _A:A['error-message']=D
	if E is not _A:A['error-info']=E
	return{'ietf-restconf:errors':{'error':[A]}}
def enc_rc_errors(encoding,errors_obj):
	B=errors_obj;A=encoding
	if A==_G:return json.dumps(B,indent=2)
	if A==_H:C=dm4errors.from_raw(B);D=C.to_xml();E=ET.tostring(D).decode(_I);F=minidom.parseString(E);return F.toprettyxml(indent='  ')
	raise NotImplementedError(_J+A)
class Encoding(Enum):json=1;xml=2
def obj_to_encoded_str(obj,enc,dm,sn,strip_wrapper=False):
	B=enc
	if B==Encoding.json:return json.dumps(obj,indent=2)
	if B==Encoding.xml:
		C=sn.from_raw(obj);D=yangson.instance.RootNode(C,sn,dm.schema_data,C.timestamp);A=D.to_xml()
		if strip_wrapper==True:assert len(A)==1;A=A[0]
		E=ET.tostring(A).decode(_I);F=minidom.parseString(E);return F.toprettyxml(indent='  ')
	raise NotImplementedError(_J+B)
def encoded_str_to_obj(estr,enc,dm,sn):
	C="Doesn't match schema: "
	if enc==Encoding.json:
		try:D=json.loads(estr)
		except Exception as A:raise Exception('JSON malformed: '+str(A))
		try:B=sn.from_raw(D)
		except Exception as A:raise Exception(C+str(A))
	elif enc==Encoding.xml:
		try:E=ET.fromstring(estr)
		except Exception as A:raise Exception('XML malformed: '+str(A))
		try:B=sn.from_xml(E)
		except Exception as A:raise Exception(C+str(A))
	else:raise NotImplementedError(_J+encoding)
	try:F=yangson.instance.RootNode(B,sn,dm.schema_data,B.timestamp)
	except Exception as A:raise Exception(C+str(A))
	try:G=F.raw_value()
	except Exception as A:raise Exception('Error transcoding: '+str(A))
	return G
def multipart_pem_to_der_dict(multipart_pem):
	A={};E=pem.parse(bytes(multipart_pem,_I))
	for F in E:
		C=F.as_text().splitlines();D=base64.b64decode(''.join(C[1:-1]));B=re.sub('-----BEGIN (.*)-----','\\g<1>',C[0])
		if B not in A:A[B]=[D]
		else:A[B].append(D)
	return A
def der_dict_to_multipart_pem(der_dict):
	D='-----\n';C=der_dict;A='';E=C.keys()
	for B in E:
		F=C[B]
		for G in F:H=base64.b64encode(G).decode('ASCII');A+='-----BEGIN '+B+D;A+=textwrap.fill(H,64)+'\n';A+='-----END '+B+D
	return A
def ders_to_degenerate_cms_obj(cert_ders):
	B=rfc5652.CertificateSet().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))
	for E in cert_ders:F,G=der_decoder.decode(E,asn1Spec=rfc5280.Certificate());assert not G;D=rfc5652.CertificateChoices();D[_N]=F;B[len(B)]=D
	A=rfc5652.SignedData();A['version']=1;A['digestAlgorithms']=rfc5652.DigestAlgorithmIdentifiers().clear();A['encapContentInfo']['eContentType']=rfc5652.id_data;A[_O]=B;C=rfc5652.ContentInfo();C[_K]=rfc5652.id_signedData;C[_P]=der_encoder.encode(A);return C
def degenerate_cms_obj_to_ders(cms_obj):
	A=cms_obj
	if A[_K]!=rfc5652.id_signedData:raise KeyError('unexpected content type: '+str(A[_K]))
	D,H=der_decoder.decode(A[_P],asn1Spec=rfc5652.SignedData());E=D[_O];B=[]
	for F in E:C=F[_N];assert type(C)==rfc5280.Certificate;G=der_encoder.encode(C);B.append(G)
	return B
def parse_raw_path(full_raw_path):
	N="' appears more than once.  RFC 8040, Section 4.8 states that each parameter can appear at most once.";M="Query parameter '";L='?';G=full_raw_path;D='=';A='/'
	if L in G:assert G.count(L)==1;B,J=G.split(L)
	else:B=G;J=_A
	if B=='':B=A
	elif B[0]!=A:raise MalformedDataPath("The datastore-specific part of the path, when present, must begin with a '/' character.")
	elif B[-1]==A:raise MalformedDataPath("Trailing '/' characters are not supported.")
	if B==A:H=A
	else:
		H='';O=B[1:].split(A)
		for E in O:
			if E=='':raise MalformedDataPath("The data path contains a superflous '/' character.")
			if D in E:assert E.count(D)==1;C,K=E.split(D);H+=A+unquote(C)+D+K
			else:H+=A+unquote(E)
	F=dict()
	if J is not _A:
		P=J.split('&')
		for I in P:
			if D in I:
				C,K=I.split(D,1)
				if C in F:raise RedundantQueryParameters(M+C+N)
				F[unquote(C)]=K
			else:
				if I in F:raise RedundantQueryParameters(M+C+N)
				F[unquote(I)]=_A
	return H,F
def check_http_headers(request,supported_media_types,accept_required):
	Q='application/yang-data+xml';P='The request method (';O=accept_required;N='missing-attribute';M='".';L='" or "';K='protocol';I='application/yang-data+json';H='Content-Type';G='text/plain';F=supported_media_types;D='Accept';B=request;assert type(F)==tuple
	if not B.body_exists:
		if any((B.method==A for A in('PUT','PATCH')))or B.method=='POST'and'ietf-datastores:running'in B.path:
			A=web.Response(status=400);C=P+B.method+') must include a request body.'
			if not D in B.headers or not any((B.headers[D]==A for A in F)):A.content_type=G;A.text=C;return A,C
			else:
				A.content_type=B.headers[D];E=gen_rc_errors(K,N,error_message=C)
				if A.content_type==I:A.text=enc_rc_errors(_G,E)
				else:A.text=enc_rc_errors(_H,E)
				return A,E
	if B.body_exists:
		if any((B.method==A for A in('GET','DELETE'))):
			A=web.Response(status=400);C=P+B.method+') should not include a request body. (enforced here)'
			if not D in B.headers or not any((B.headers[D]==A for A in F)):A.content_type=G;A.text=C;return A,C
			else:
				A.content_type=B.headers[D];E=gen_rc_errors(K,N,error_message=C)
				if A.content_type==I:A.text=enc_rc_errors(_G,E)
				else:A.text=enc_rc_errors(_H,E)
				return A,E
		if not H in B.headers:
			A=web.Response(status=400);C='A "Content-Type" value must be specified when a request body is passed. The "Content-Type" value must be "application/yang-data+json" or "application/yang-data+xml".'
			if not D in B.headers or not any((B.headers[D]==A for A in F)):A.content_type=G;A.text=C;return A,C
			else:
				A.content_type=B.headers[D];E=gen_rc_errors(K,N,error_message=C)
				if A.content_type==I:A.text=enc_rc_errors(_G,E)
				else:A.text=enc_rc_errors(_H,E)
				return A,E
		if not any((B.headers[H]==A for A in F)):
			A=web.Response(status=400);C='The "Content-Type" value, when specified, must be "'+L.join(F)+'". Got: "'+B.headers[H]+M
			if not D in B.headers or not any((B.headers[D]==A for A in(I,Q))):A.content_type=G;A.text=C;return A,C
			else:
				A.content_type=B.headers[D];E=gen_rc_errors(K,'bad-attribute',error_message=C)
				if A.content_type==I:A.text=enc_rc_errors(_G,E)
				else:A.text=enc_rc_errors(_H,E)
				return A,E
	J=_A
	if D not in B.headers or B.headers[D]=='*/*':
		if H not in B.headers:
			if O:A=web.Response(status=406);C='Unable to determine response encoding; neither "Accept" nor "Content-Type" specified.  An "Accept" value should be specified, and have the value "'+L.join(F)+M;A.content_type=G;A.text=C;return A,C
			J=G
		elif not any((B.headers[H]==A for A in(I,Q))):
			if O:A=web.Response(status=406);C='Unable to determine response encoding; "Accept" not specified and the "Content-Type" specified ('+B.headers[H]+') is invalid.  An "Accept" value should be specified, and have the value "'+L.join(F)+M;A.content_type=G;A.text=C;return A,C
			J=G
		else:J=B.headers[H]
	elif not any((B.headers[D]==A for A in F)):A=web.Response(status=406);C='Unable to determine response encoding; the "Accept" value specified ('+B.headers[D]+') is invalid.  The "Accept" value, when specified, must have the value "'+L.join(F)+M;A.content_type=G;A.text=C;return A,C
	else:J=B.headers[D]
	return J,_A