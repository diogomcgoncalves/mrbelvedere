import json
import re
import requests
import zipfile
import StringIO

# Zip Utilities
def zip_subfolder(zip_src, path, namespace_token=None, namespace=None):
    if not path.endswith('/'):
        path = path + '/'

    if namespace_token:
        # The default namespace token for CumulusCI is %%%NAMESPACE%%% but that doesn't
        # work well with filenames so replace all %'s with _'s for the filename token
        filename_namespace_token = namespace_token.replace('%','_')

    # Handle the %%%NAMESPACE_OR_C%%% token
    namespace_or_c_token = '%%%NAMESPACE_OR_C%%%'

    # Handle the %%%NAMESPACED_ORG%%% token
    namespaced_org_token = '%%%NAMESPACED_ORG%%%'

    zip_dest = zipfile.ZipFile(StringIO.StringIO(), 'w', zipfile.ZIP_DEFLATED)
    for name in zip_src.namelist():
        if not name.startswith(path):
            continue

        content = zip_src.read(name)
        rel_name = name.replace(path, '', 1)

        # Strip the NAMESPACED_ORG token since we don't support it in mrbelvedere
        content = content.replace(namespaced_org_token, '')
        if namespace_token:
            # If a namespace_token was specified, replace the token with the namespace or nothing
            if namespace:
                content = content.replace(namespace_token, '%s__' % namespace)
                content = content.replace(namespace_or_c_token, '%s' % namespace)
                if rel_name:
                    rel_name = rel_name.replace(filename_namespace_token, '%s__' % namespace)
            else:
                content = content.replace(namespace_token, '')
                content = content.replace(namespace_or_c_token, 'c')
                if rel_name:
                    rel_name = rel_name.replace(filename_namespace_token, '')

        if rel_name:
            zip_dest.writestr(rel_name, content)

    return zip_dest

def zip_subfolders(zip_src, path, namespace_token=None, namespace=None):
    if not path.endswith('/'):
        path = path + '/'

    if namespace_token:
        # The default namespace token for CumulusCI is %%%NAMESPACE%%% but that doesn't
        # work well with filenames so replace all %'s with _'s for the filename token
        filename_namespace_token = namespace_token.replace('%','_')

    zips = {}
    for name in zip_src.namelist():
        if not name.startswith(path):
            continue

        name_parts = name.replace(path, '', 1).split('/')
   
        # Skip files at the root of the path, we only want files inside subfolders
        if len(name_parts) == 1:
            continue

        # Skip the subdirectory itself
        if len(name_parts) == 2 and name_parts[-1] == '':
            name_parts.pop()

        # Get or create the subfolder's zip file in memory
        subfolder = name_parts[0]
        if subfolder not in zips:
            zips[subfolder] = zipfile.ZipFile(StringIO.StringIO(), 'w', zipfile.ZIP_DEFLATED)
       
        # Write the file 
        content = zip_src.read(name)

        zip_name = '/'.join(name_parts[1:])

        if namespace_token:
            # If a namespace_token was specified, replace the token with the namespace or nothing
            if namespace:
                content = content.replace(namespace_token, '%s__' % namespace)
                zip_name = zip_name.replace(filename_namespace_token, '%s__' % namespace)
            else:
                content = content.replace(namespace_token, '')
                zip_name = zip_name.replace(filename_namespace_token, '')
    
        zips[subfolder].writestr(zip_name, content)

    return zips

# Salesforce related utilities

# From https://gist.github.com/KorbenC/7356677
def convert_to_18(id):
    #check valid input
    if id is None:
        return id
    if len(id) < 15:
        print "not a valid 15 digit ID"
        return
    #print initial id
    print "15 digit ID: ", id
    suffix = ''
    for i in xrange(0, 3):
        flags = 0
        for x in xrange(0,5):
            c = id[i*5+x]
            #add flag if c is uppercase
            if c.upper() == c and c >= 'A' and c <= 'Z':
                flags = flags + (1 << x)
        if flags <= 25:
            suffix = suffix + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[flags]
        else:
            suffix = suffix + '012345'[flags - 26]
    return id + suffix

def obscure_salesforce_log(text):
    text = obscure_mpinstaller_deployment_test_failure(text)
    text = obscure_salesforce_ids(text)
    text = obscure_salesforce_limit_details(text)
    text = obscure_salesforce_error_id(text)
    text = obscure_salesforce_org_name(text)
    text = obscure_salesforce_created_by_name(text)
    return text

def obscure_mpinstaller_deployment_test_failure(text):
    """ Returns 'Apex Test Failure' as the error text if the text contains a test failure message. """
    if text.find('Apex Test Failure: ') != -1:
        return 'Apex Test Failure'
    return text

def obscure_salesforce_limit_details(text):
    return re.sub(r'(\(Required: )[0-9]{1,4}(, Available: )[0-9]{1,4}(\))', r'\1<X>\2<Y>\3', text)

def obscure_salesforce_error_id(text):
    # FIXME: verify the length ranges for the error number
    return re.sub(r'(Please include this ErrorId if you contact support: )([0-9]{6,18}-[0-9]{3,10} \([0-9]{6,14}\))', r'\1<ERROR_ID>', text)

def obscure_salesforce_org_name(text):
    return re.sub(r'(Organization Name: )(.*)(\nOrganization ID:)', r'\1<ORG_NAME>\3', text) 

def obscure_salesforce_ids(text):
    # Find all possible ids and split the first 3 characters out
    matches = re.findall(r'([a-zA-Z0-9]{3})([a-zA-Z0-9]{12}|[a-zA-Z0-9]{15})', text)
   
    replace = [] 
    for match in matches:
        if match[0] in SALESFORCE_OID_PREFIXES:
            replace_t = ('%s%s' % match, '%s...' % match[0])
            if replace_t not in replace:
                replace.append(replace_t)
    
    for replace_t in replace:
        text = text.replace(replace_t[0], replace_t[1])

    return text

def obscure_salesforce_created_by_name(text):
    return re.sub(r'<createdByName>.*</createdByName>','', text)

# Taken from http://www.fishofprey.com/2011/09/obscure-salesforce-object-key-prefixes.html
SALESFORCE_OID_PREFIXES = [
'000',
'001',
'002',
'003',
'005',
'006',
'007',
'008',
'00B',
'00D',
'00E',
'00G',
'00I',
'00J',
'00K',
'00N',
'00O',
'00P',
'00Q',
'00S',
'00T',
'00U',
'00X',
'00Y',
'00a',
'Use',
'00a',
'Use',
'00b',
'00c',
'00e',
'00h',
'00i',
'00j',
'00k',
'00l',
'00o',
'00p',
'00q',
'00r',
'00s',
'00t',
'00u',
'00v',
'010',
'011',
'012',
'013',
'014',
'015',
'016',
'017',
'018',
'019',
'01A',
'01B',
'01C',
'01D',
'01G',
'01H',
'01I',
'01J',
'01N',
'01P',
'01Q',
'01R',
'01S',
'01T',
'01U',
'01V',
'01W',
'01X',
'01Y',
'01Z',
'01a',
'01b',
'01c',
'01e',
'01h',
'01j',
'01k',
'01l',
'01m',
'01n',
'01o',
'01p',
'01q',
'01r',
'01s',
'01t',
'01u',
'01v',
'01w',
'01y',
'01z',
'020',
'022',
'023',
'024',
'025',
'026',
'02A',
'02B',
'02C',
'02D',
'02F',
'02T',
'02U',
'02V',
'02X',
'02Y',
'02Z',
'02a',
'02b',
'02c',
'02f',
'02g',
'02h',
'02i',
'02k',
'02m',
'02n',
'02o',
'02p',
'02q',
'02r',
'02t',
'02u',
'02v',
'02w',
'02x',
'02y',
'02z',
'033',
'034',
'035',
'036',
'037',
'038',
'039',
'03D',
'03G',
'03H',
'03I',
'03J',
'03K',
'03M',
'03N',
'03a',
'03c',
'03d',
'03e',
'03f',
'03g',
'03i',
'03j',
'03k',
'03n',
'03q',
'03s',
'03u',
'040',
'043',
'044',
'045',
'04Y',
'04Z',
'04a',
'04b',
'04c',
'04d',
'04e',
'04f',
'04g',
'04h',
'04i',
'04j',
'04k',
'04l',
'04m',
'04n',
'04o',
'04p',
'04q',
'04r',
'04s',
'04t',
'04u',
'04v',
'04x',
'04z',
'04V',
'04P',
'050',
'051',
'052',
'053',
'054',
'055',
'056',
'057',
'058',
'059',
'05A',
'05B',
'05C',
'05G',
'05I',
'05J',
'05K',
'05L',
'05N',
'05P',
'05Q',
'05R',
'05S',
'05T',
'05U',
'05V',
'05W',
'05X',
'05Z',
'05t',
'060',
'061',
'062',
'063',
'064',
'065',
'066',
'067',
'068',
'069',
'06A',
'06B',
'06G',
'06N',
'06O',
'06P',
'070',
'071',
'072',
'073',
'076',
'078',
'079',
'07A',
'07D',
'07E',
'07F',
'07G',
'07J',
'07K',
'07L',
'07M',
'07O',
'07P',
'07R',
'07T',
'07U',
'07V',
'07Y',
'07Z',
'07e',
'07n',
'080',
'081',
'082',
'083',
'084',
'085',
'086',
'087',
'08E',
'08F',
'08a',
'08d',
'08e',
'08g',
'08s',
'090',
'091',
'092',
'093',
'094',
'095',
'096',
'097',
'099',
'09A',
'09B',
'09D',
'09F',
'09H',
'09I',
'09J',
'09S',
'09T',
'09U',
'09V',
'09a',
'0A0',
'0A1',
'0A2',
'0A3',
'0A4',
'0A5',
'0A7',
'0A8',
'0A9',
'0AB',
'0AD',
'0AH',
'0AI',
'0AL',
'0AM',
'0AN',
'0AT',
'0AU',
'0AW',
'0AX',
'0AZ',
'0Af',
'0Ai',
'0Aj',
'0Ak',
'0Al',
'0B0',
'0B1',
'0B2',
'0B3',
'0B9',
'0BA',
'0BB',
'0BC',
'0BE',
'0BF',
'0BG',
'0BH',
'0BI',
'0BJ',
'0BL',
'0BM',
'0BR',
'0BV',
'0BW',
'0BX',
'0BY',
'0BZ',
'0Ba',
'0Bb',
'0Bc',
'0Bd',
'0Be',
'0Bf',
'0Bi',
'0Bk',
'0Bl',
'0C0',
'0C2',
'0C8',
'0CC',
'0CF',
'0CI',
'0CJ',
'0CL',
'0CS',
'0Ci',
'0D1',
'0D2',
'0D3',
'0D4',
'0D5',
'Use',
'0D6',
'0D7',
'0D8',
'0D9',
'0DA',
'0DC',
'0DD',
'0DE',
'0DF',
'0DG',
'0DH',
'0DM',
'0DN',
'0DR',
'0DS',
'0DT',
'0DU',
'0DV',
'0DX',
'0DY',
'0Db',
'0Df',
'0E0',
'0E1',
'0E2',
'0E3',
'0E4',
'0E5',
'0E6',
'0E8',
'0EA',
'0EB',
'0EG',
'0EH',
'0EI',
'0EJ',
'0EM',
'0EO',
'0EP',
'0EQ',
'0ER',
'0EV',
'0Eb',
'0Ee',
'0Ef',
'0Eg',
'0F0',
'0F3',
'0F5',
'0F7',
'0F8',
'0F9',
'0FA',
'0FB',
'0FG',
'0FH',
'0FM',
'0FO',
'0FP',
'0FQ',
'0FR',
'0FT',
'0Fa',
'0G1',
'0G8',
'0G9',
'0GC',
'0GD',
'0GE',
'0GH',
'0GI',
'0GJ',
'0H0',
'0H1',
'0H4',
'0H7',
'0HF',
'0HG',
'0HI',
'0HN',
'0HO',
'0HR',
'0Hi',
'0Hj',
'0Hk',
'0Hl',
'0I0',
'0I2',
'0I3',
'0I4',
'0I5',
'0I6',
'0I7',
'0I8',
'0I9',
'0IA',
'0IB',
'0IC',
'0ID',
'0IF',
'0II',
'0IO',
'0IS',
'0IV',
'0IX',
'0IY',
'0Ih',
'0Ii',
'0Ij',
'0Ik',
'0In',
'0Io',
'0J0',
'0J2',
'0J4',
'0J5',
'0J8',
'0JS',
'0Jf',
'0K0',
'0K2',
'0K3',
'0LD',
'0LG',
'0LN',
'0M1',
'0ME',
'0MF',
'0MJ',
'0O0',
'0P0',
'0P1',
'0P2',
'0PF',
'0PL',
'0PQ',
'0PS',
'0Pa',
'0Q0',
'0Qc',
'0RA',
'0RE',
'0RT',
'0SO',
'0TI',
'0TO',
'0TY',
'0Tt',
'0XC',
'0XU',
'0Ya',
'0Ym',
'0Ys',
'0Yu',
'0Yw',
'0ca',
'0cs',
'0e1',
'0eb',
'0hc',
'0hd',
'0ht',
'0in',
'0ns',
'0rp',
'0sp',
'0tR',
'0tS',
'0te',
'0tg',
'0tr',
'0ts',
'0tu',
'100',
'101',
'102',
'10y',
'10z',
'110',
'111',
'112',
'113',
'11a',
'1ci',
'1cl',
'1dc',
'1de',
'1do',
'1dp',
'1dr',
'204',
'2LA',
'300',
'301',
'308',
'309',
'30A',
'30C',
'30D',
'30F',
'30L',
'30Q',
'30R',
'30S',
'30V',
'30a',
'30c',
'30d',
'30f',
'30g',
'30m',
'30r',
'30t',
'30v',
'310',
'31A',
'31C',
'31S',
'31V',
'31c',
'31d',
'31i',
'31o',
'31v',
'3M1',
'3M3',
'3M4',
'3M5',
'3M6',
'3MA',
'3MC',
'3MD',
'3MF',
'3MG',
'3MH',
'3MI',
'3MJ',
'400',
'401',
'402',
'403',
'4A0',
'4F0',
'4F1',
'4F2',
'4F3',
'500',
'501',
'5Sp',
'5CS',
'608',
'6AA',
'6AB',
'6AC',
'6AD',
'701',
'707',
'708',
'709',
'710',
'711',
'712',
'713',
'714',
'715',
'716',
'729',
'737',
'750',
'751',
'752',
'753',
'754',
'766',
'777',
'7tf',
'800',
'806',
'80D',
'888',
'ka0',
'X00',
]
