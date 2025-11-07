#!/usr/bin/env python3
import requests
import socket
import ssl
import os

def query_livestatus_local(site_name, query):
    """Query local Livestatus via Unix socket"""
    socket_path = f"/omd/sites/{site_name}/tmp/run/live"
    
    try:
        if not os.path.exists(socket_path):
            return None
        
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(socket_path)
        
        if not query.endswith('\n'):
            query += '\n'
        sock.sendall(query.encode('utf-8'))
        sock.shutdown(socket.SHUT_WR)
        
        response = b""
        sock.settimeout(2)
        
        try:
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                response += data
        except socket.timeout:
            pass
        
        sock.close()
        
        result = response.decode('utf-8', errors='ignore').strip()
        
        for line in result.split('\n'):
            line = line.strip()
            if line and line.isdigit():
                return line
        
        return result if result else None
        
    except Exception as e:
        print(f"  Warning: Error querying local site: {e}")
        return None

def query_livestatus_ssl(host, port, query, timeout=10):
    """Query remote Livestatus over SSL connection"""
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        ssl_sock = context.wrap_socket(sock)
        
        ssl_sock.connect((host, port))
        
        if not query.endswith('\n'):
            query += '\n'
        ssl_sock.sendall(query.encode('utf-8'))
        
        response = b""
        ssl_sock.settimeout(5)
        
        try:
            while True:
                data = ssl_sock.recv(4096)
                if not data:
                    break
                response += data
        except socket.timeout:
            pass
        
        ssl_sock.close()
        
        result = response.decode('utf-8', errors='ignore').strip()
        
        for line in result.split('\n'):
            line = line.strip()
            if line and line.isdigit():
                return line
        
        return result if result else None
        
    except Exception as e:
        print(f"  Warning: Error: {e}")
        return None

def get_site_connections(host_name, site_name, username, password, proto="http"):
    """Get all site connections from CheckMK API"""
    
    api_url = f"{proto}://{host_name}/{site_name}/check_mk/api/1.0"
    
    session = requests.session()
    session.headers['Authorization'] = f"Bearer {username} {password}"
    session.headers['Accept'] = 'application/json'
    
    resp = session.get(
        f"{api_url}/domain-types/site_connection/collections/all",
    )
    
    if resp.status_code != 200:
        raise RuntimeError(f"API Error: {resp.status_code}")
    
    data = resp.json()
    sites = []
    
    for site in data.get('value', []):
        extensions = site.get('extensions', {})
        
        site_id = extensions.get('basic_settings', {}).get('site_id')
        connection = extensions.get('status_connection', {}).get('connection', {})
        socket_type = connection.get('socket_type')
        
        if socket_type == 'local':
            sites.append({
                'site_id': site_id,
                'type': 'local'
            })
        elif socket_type in ['tcp', 'unix']:
            host = connection.get('host')
            port = connection.get('port')
            encrypted = connection.get('encrypted', False)
            
            if site_id and host and port:
                sites.append({
                    'site_id': site_id,
                    'type': 'remote',
                    'host': host,
                    'port': port,
                    'encrypted': encrypted
                })
    
    return sites

if __name__ == "__main__":
    HOST_NAME = "192.168.123.112"
    SITE_NAME = "provider"
    USERNAME = "cmkadmin"
    PASSWORD = "cmk"
    
    print("=" * 70)
    print(" CheckMK Sites Statistics")
    print("=" * 70)
    
    sites = get_site_connections(HOST_NAME, SITE_NAME, USERNAME, PASSWORD)
    
    all_sites_data = []
    
    for site in sites:
        site_id = site['site_id']
        print(f"\nSite: {site_id}")
        
        if site['type'] == 'local':
            print(f"   Type: Local")
            
            hosts_count = query_livestatus_local(SITE_NAME, "GET hosts\nStats: state >= 0\n")
            services_count = query_livestatus_local(SITE_NAME, "GET services\nStats: state >= 0\n")
            
        else:
            host = site['host']
            port = site['port']
            encrypted = site.get('encrypted', False)
            
            print(f"   Type: Remote")
            print(f"   Connection: {host}:{port} {'(SSL)' if encrypted else '(Plain)'}")
            
            if encrypted:
                hosts_query = "GET hosts\nStats: state ~ *\n"
                services_query = "GET services\nStats: state ~ *\n"
                
                hosts_count = query_livestatus_ssl(host, port, hosts_query)
                services_count = query_livestatus_ssl(host, port, services_query)
            else:
                hosts_count = services_count = None
                print("   Warning: Plain TCP not supported")
        
        if hosts_count and services_count:
            print(f"   Hosts: {hosts_count} | Services: {services_count}")
            all_sites_data.append({
                'site_id': site_id,
                'type': site['type'],
                'hosts': int(hosts_count),
                'services': int(services_count)
            })
        else:
            print(f"   Failed: Query failed")
    
    if all_sites_data:
        print("\n" + "=" * 70)
        print(" Summary")
        print("=" * 70)
        
        local = sum(1 for s in all_sites_data if s['type'] == 'local')
        remote = sum(1 for s in all_sites_data if s['type'] == 'remote')
        
        print(f"Sites: {len(all_sites_data)} (Local: {local}, Remote: {remote})")
        print(f"Total Hosts: {sum(s['hosts'] for s in all_sites_data)}")
        print(f"Total Services: {sum(s['services'] for s in all_sites_data)}")
        print("=" * 70)
