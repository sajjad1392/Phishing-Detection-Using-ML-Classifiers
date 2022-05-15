from lib.functions import *
import posixpath
import csv


def attributes():
    """Output file attributes."""
    lexical = ['URLs', 
                'comma_url', 'dot_url', 'hyphe_url', 'slash_url', 'dollar_url', 'percent_url', 'underscore_url', 'plus_url', 'equal_url', 'ampersand_url', 'at_url', 'question_url', 'amp_greater_equal', 'hashtag_url', 'colon_url', 'http_url', 'www_url', 'delims_url', 'other_delims_url', 'other_delims_url2', 'len_url', 'email_exist', 'count_tld_url', 'protocol_url', 'double_slash_pos', 'suspwords_url', 'brand_url', 'digits_url', 'entropy_url',
                'dot_host', 'dot_subdomain', 'hyphe_host', 'hyphe_domain', 'prefix_suffix', 'underscore_host', 'delims_host', 'other_delims_host', 'other_delims_host2', 'len_host', 'len_domain', 'len_subdomain', 'ip_exist', 'having_https', 'suspwords_host', 'suspwords_subdomain', 'brand_host', 'brand_subdomain', 'digits_host', 'digits_domain', 'digits_subdomain', 'entropy_host', 'entropy_subdomain', 'url_token_count', 'url_avg_tok', 'url_large_tok', 'host_token_count', 'host_avg_tok', 'host_large_tok', 'path_token_count', 'path_avg_tok', 'path_large_tok', 'frag_token_count', 'frag_avg_tok', 'frag_large_tok',
                'dot_path', 'hyphe_path', 'slash_path', 'delims_path', 'len_path', 'tld_path', 'suspwords_path', 'brand_path', 'digits_path', 'entropy_path',
                'len_file', 'extension', 'suspwords_file', 'brand_file',
                'dot_params', 'hyphe_params', 'slash_params', 'delims_params', 'len_params', 'number_params', 'suspwords_params', 'brand_params', 'digits_params', 'entropy_params', 
                'dot_frag', 'hyphe_frag', 'slash_frag', 'underline_frag', 'colon_path', 'http_path', 'www_path', 'delims_frag', 'other_delims_frag', 'other_delims_frag2', 'len_frag', 'suspwords_frag', 'brand_frag', 'digits_frag', 'entropy_frag'
    ]

    others = ['tiny_url', 'ratio_url_path', 'ratio_url_host']

    list_attributes = []
    list_attributes.extend(lexical)
    list_attributes.extend(others)
    list_attributes.extend(['class'])

    return list_attributes


def main(urls, dataset):
    with open(dataset, "w", newline='') as output:
        writer = csv.writer(output)
        writer.writerow(attributes())
        count_url = 0
        for url in read_file(urls):
            # print(url)
            uu = url.replace(',', '').replace('"', '')
            #uu = url.strip().split(',')
            #oname = uu[0]
            #olabel = uu[1]
            
            count_url = count_url + 1
            dict_url = start_url(uu)
            
            """LEXICAL"""
            # URL
            comma_url = count(url, ',')
            if comma_url > 0:
                comma_url = 1
            else:
                comma_url = 0
                
            dot_url = str(count(dict_url['url'], '.'))
            hyphe_url = str(count(dict_url['url'], '-'))
            slash_url = str(count(dict_url['url'], '/'))
            dollar_url = count(dict_url['url'], '$')
            percent_url = count(dict_url['url'], '%')
            underscore_url = count(dict_url['url'], '_')
            plus_url = count(dict_url['url'], '+')
            equal_url = count(dict_url['url'], '=')
            ampersand_url = count(dict_url['url'], '&')
            at_url = count(dict_url['url'], '@')
            if at_url > 0:
                at_url = 1
            else:
                at_url = 0
                
            question_url = count(dict_url['url'], '?')
            if question_url > 0:
                question_url = 1
            else:
                question_url = 0
                
            amp_greater_equal = 0
            if ampersand_url > equal_url:
                amp_greater_equal = 1
            else:
                amp_greater_equal = 0
                
            hashtag_url = count(dict_url['url'], '#')
            if hashtag_url > 1:
                hashtag_url = 1
            else:
                hashtag_url = 0
                
            colon_url = count(dict_url['url'], ':')
            if colon_url > 0:
                colon_url = 1
            else:
                colon_url = 0
              
            http_url = count(dict_url['url'], 'http')
            if http_url > 0:
                http_url = 1
            else:
                http_url = 0
                
            www_url = count(dict_url['url2'], 'www')
            if www_url > 0:
                www_url = 1
            else:
                www_url = 0
            
            delims_url = str(count_delims(dict_url['url']))
            other_delims_url = str(other_delims(dict_url['url']))
            other_delims_url2 = str(other_delims2(dict_url['url']))
            len_url = length(dict_url['url'])
            email_exist = str(valid_email(dict_url['url']))
            count_tld_url = count_tld(dict_url['url'])
            protocol_url = str(having_protocol(dict_url['url2']))
            double_slash_pos = str(slash_pos(dict_url['protocol'] + dict_url['url']))
            suspwords_url = str(check_suspwords(dict_url['url']))
            brand_url = str(check_brand(dict_url['url']))
            digits_url = str(count_degits(dict_url['url']))
            entropy_url = str(entropy(dict_url['url']))
            
            # DOMAIN
            dot_host = str(count(dict_url['host'], '.'))
            dot_subdomain = count(dict_url['subdomain'], '.')  
            hyphe_host = str(count(dict_url['host'], '-'))
            hyphe_domain = count(dict_url['domain'], '-')
            if hyphe_domain > 1:
                hyphe_domain = 1
            else:
                hyphe_domain = 0
                
            prefix_suffix = str(prefixSuffix(dict_url['protocol'] + dict_url['url']))
            underscore_host = count(dict_url['host'], '_')
            if underscore_host > 0:
                underscore_host = 1
            else:
                underscore_host = 0
 
            delims_host = str(count_delims(dict_url['host']))
            other_delims_host = str(other_delims(dict_url['host']))
            other_delims_host2 = str(other_delims2(dict_url['host']))
            len_host = length(dict_url['host'])
            len_domain = length(dict_url['domain'])
            len_subdomain = length(dict_url['subdomain'])
            ip_exist = str(valid_ip(dict_url['host']))
            having_https = str(is_https(dict_url['protocol'] + dict_url['url']))
            suspwords_host = str(check_suspwords(dict_url['host']))
            suspwords_subdomain = str(check_suspwords(dict_url['subdomain']))
            brand_host = str(check_brand(dict_url['host']))
            brand_subdomain = str(check_brand(dict_url['subdomain']))
            digits_host = str(count_degits(dict_url['host']))
            digits_domain = str(count_degits(dict_url['domain']))
            digits_subdomain = str(count_degits(dict_url['subdomain']))
            entropy_host = str(entropy(dict_url['host']))
            entropy_subdomain = str(entropy(dict_url['subdomain']))
                        
            url_token_count, url_avg_tok, url_large_tok = avg_large_count(dict_url['url'])
            host_token_count, host_avg_tok, host_large_tok = avg_large_count(dict_url['host'])
            path_token_count, path_avg_tok, path_large_tok = avg_large_count(dict_url['path'])
            frag_token_count, frag_avg_tok, frag_large_tok = avg_large_count(dict_url['fullpath'])
            
            # DIRECTORY
            if dict_url['path']:
                dot_path = str(count(dict_url['path'], '.'))
                hyphe_path = str(count(dict_url['path'], '-'))
                slash_path = str(count(dict_url['path'], '/'))
                delims_path = str(count_delims(dict_url['path']))
                len_path = length(dict_url['path'])
                tld_path = str(check_tld(dict_url['fullpath']))
                suspwords_path = str(check_suspwords(dict_url['path']))
                brand_path = str(check_brand(dict_url['path']))
                digits_path = str(count_degits(dict_url['path']))
                entropy_path = str(entropy(dict_url['path']))
                
                #file
                len_file = length(posixpath.basename(dict_url['path']))
                extension = str(extract_extension(posixpath.basename(dict_url['path'])))
                suspwords_file = str(check_suspwords(posixpath.basename(dict_url['path'])))
                brand_file = str(check_brand(posixpath.basename(dict_url['path'])))
                
                #Full path
                dot_frag = str(count(dict_url['fullpath'], '.'))
                hyphe_frag = str(count(dict_url['fullpath'], '-'))
                slash_frag = str(count(dict_url['fullpath'], '/'))
                underline_frag = str(count(dict_url['fullpath'], '_'))
                colon_path = count(dict_url['fullpath'], ':')
                if colon_path > 0:
                    colon_path = 1
                else:
                    colon_path = 0
                    
                http_path = count(dict_url['fullpath'], 'http')
                if http_path > 0:
                    http_path = 1
                else:
                    http_path = 0
                    
                www_path = count(dict_url['fullpath'], 'www')
                if www_path > 0:
                    www_path = 1
                else:
                    www_path = 0
                    
                delims_frag = str(count_delims(dict_url['fullpath']))
                other_delims_frag = str(other_delims(dict_url['fullpath']))
                other_delims_frag2 = str(other_delims2(dict_url['fullpath']))
                len_frag = str(length(dict_url['fullpath']))
                suspwords_frag = str(check_suspwords(dict_url['fullpath']))
                brand_frag = str(check_brand(dict_url['fullpath']))
                digits_frag = str(count_degits(dict_url['fullpath']))
                entropy_frag = str(entropy(dict_url['fullpath']))
            else:
                dot_path = '0'
                hyphe_path = '0'
                slash_path = '0'
                delims_path = '0'
                len_path = 0
                tld_path = '0'
                suspwords_path = '0'
                brand_path = '0'
                digits_path = '0'
                entropy_path = '0'
                len_file = 0
                extension = '0'
                suspwords_file = '0'
                brand_file = '0'
                dot_frag = '0'
                hyphe_frag = '0'
                slash_frag = '0'
                underline_frag = '0'
                colon_path = 0
                http_path = 0
                www_path = 0
                delims_frag = '0'
                other_delims_frag = '0'
                other_delims_frag2 = '0'
                len_frag = '0'
                suspwords_frag = '0'
                brand_frag = '0'
                digits_frag = '0'
                entropy_frag = '0'
                
            # PARAMETERS
            if dict_url['query']:
                dot_params = str(count(dict_url['query'], '.'))
                hyphe_params = str(count(dict_url['query'], '-'))
                slash_params = str(count(dict_url['query'], '/'))
                delims_params = str(count_delims(dict_url['query']))
                len_params = length(dict_url['query'])
                number_params = str(count_params(dict_url['query']))
                suspwords_params = str(check_suspwords(dict_url['query']))
                brand_params = str(check_brand(dict_url['query']))
                digits_params = str(count_degits(dict_url['query']))
                entropy_params = str(entropy(dict_url['query']))
            else:
                dot_params = '0'
                hyphe_params = '0'
                slash_params = '0'
                delims_params = '0'
                len_params = 0
                number_params = '0'
                suspwords_params = '0'
                brand_params = '0'
                digits_params = '0'
                entropy_params = '0'
            
            tiny_url = str(tinyURL(dict_url['url']))
            ratio_url_path = int(round((len_path/len_url)))
            ratio_url_host = int(round((len_host/len_url)))
            #ratio_path_host = int(round((len_path/len_host)))
            
            #ratio_url_path2 = len_path/len_url
            #ratio_url_host2 = len_host/len_url
            #ratio_path_host2 = len_path/len_host
            
            _lexical = [uu, comma_url, 
                dot_url, hyphe_url, slash_url, dollar_url, percent_url, underscore_url, plus_url, equal_url, ampersand_url, at_url, question_url, amp_greater_equal, hashtag_url, colon_url, http_url, www_url, delims_url, other_delims_url, other_delims_url2, len_url, email_exist, count_tld_url, protocol_url, double_slash_pos, suspwords_url, brand_url, digits_url, entropy_url, 
                dot_host, dot_subdomain, hyphe_host, hyphe_domain, prefix_suffix, underscore_host, delims_host, other_delims_host, other_delims_host2, len_host, len_domain, len_subdomain, ip_exist, having_https, suspwords_host, suspwords_subdomain, brand_host, brand_subdomain, digits_host, digits_domain, digits_subdomain, entropy_host, entropy_subdomain, url_token_count, url_avg_tok, url_large_tok, host_token_count, host_avg_tok, host_large_tok, path_token_count, path_avg_tok, path_large_tok, frag_token_count, frag_avg_tok, frag_large_tok,
                dot_path, hyphe_path, slash_path, delims_path, len_path, tld_path, suspwords_path, brand_path, digits_path, entropy_path,
                len_file, extension, suspwords_file, brand_file,
                dot_params, hyphe_params, slash_params, delims_params, len_params, number_params, suspwords_params, brand_params, digits_params, entropy_params,
                dot_frag, hyphe_frag, slash_frag, underline_frag, colon_path, http_path, www_path, delims_frag, other_delims_frag, other_delims_frag2, len_frag, suspwords_frag, brand_frag, digits_frag, entropy_frag
            ]
            
            _others = [tiny_url, ratio_url_path, ratio_url_host]

            result = []
            result.extend(_lexical)
            result.extend(_others)
            result.extend([''])

            writer.writerow(result)
            
            print(count_url)
            print(dict_url['url'])
