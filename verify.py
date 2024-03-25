#!/usr/bin/env python

import copy
import json
import os
import os.path
import sys

import keri.app.habbing
import keri.core.coring
import keri.vdr.credentialing
import keri.vdr.verifying

archive_directory = sys.argv[1].removesuffix('/')

def compact(expanded_json):
    expanded_json = copy.deepcopy(expanded_json)

    markdown = expanded_json['a']['markdown']['values']
    for filename, details in markdown.items():
        qb64 = details['d']
        saider = keri.core.coring.Saider(sad=details)
        if qb64 != saider.qb64:
            print(f'Invalid SAID {qb64} found for {filename} details.')
        markdown[filename] = qb64

    markdown = expanded_json['a']['markdown']
    saider = keri.core.coring.Saider(sad=markdown)
    expanded_json['a']['markdown'] = saider.qb64

    assets = expanded_json['a']['assets']['values']
    for filename, details in assets.items():
        qb64 = details['d']
        saider = keri.core.coring.Saider(sad=details)
        if qb64 != saider.qb64:
            print(f'Invalid SAID {qb64} found for {filename} details.')
        assets[filename] = qb64

    assets = expanded_json['a']['assets']
    saider = keri.core.coring.Saider(sad=assets)
    expanded_json['a']['assets'] = saider.qb64

    attrib = expanded_json['a']
    saider = keri.core.coring.Saider(sad=attrib)
    expanded_json['a'] = saider.qb64

    expanded_json['r']['liabilityDisclaimer'] = expanded_json['r']['liabilityDisclaimer']['d']
    expanded_json['r']['verificationInstructions'] = expanded_json['r']['verificationInstructions']['d']
    
    rules = expanded_json['r']
    saider = keri.core.coring.Saider(sad=rules)
    expanded_json['r'] = saider.qb64

    saider = keri.core.coring.Saider(sad=expanded_json)
    expanded_json['d'] = saider.qb64

    return saider.qb64

with keri.app.habbing.openHab(name='temp', temp=True) as (hby, hab):
    rgy = keri.vdr.credentialing.Regery(hby=hby, name='temp', base='', temp=True)
    vry = keri.vdr.verifying.Verifier(hby=hby, reger=rgy.reger)
    hby.psr.vry = vry
    hby.psr.tvy = vry.tvy

    print('No further output indicates success!')

    schema_directory = os.path.join(archive_directory, 'schemas')
    schema_paths = [
        os.path.join(schema_directory, f)
        for f in os.listdir(schema_directory) 
        if os.path.isfile(os.path.join(schema_directory, f))
    ]

    for path in schema_paths:
        with open(path, 'r') as schema_file:
            schema_json = schema_file.read()
            schema_id = json.loads(schema_json)['$id']
            vry.resolver.add(schema_id, schema_json.encode())

    ceg_acdc_saids = set()
    ceg_paths = [
        os.path.join(archive_directory, f)
        for f in os.listdir(archive_directory)
        if f.endswith('.ceg') and os.path.isfile(os.path.join(archive_directory, f))
    ]

    if not ceg_paths:
        print("No .ceg files found!")

    for ceg_path in ceg_paths:
        with open(ceg_path, 'rb') as ceg_file:
            messages = ceg_file.read()
            hby.psr.parse(bytearray(messages))
            ceg_acdc_saids.add(ceg_path.split('/')[-1].split('.')[0])

    expanded_acdc_paths = [
        os.path.join(archive_directory, f)
        for f in os.listdir(archive_directory)
        if f.endswith('.acdc') and os.path.isfile(os.path.join(archive_directory, f))
    ]

    if not expanded_acdc_paths:
        print("No .acdc files found!")

    for acdc_path in expanded_acdc_paths:
        with open(acdc_path, 'r') as acdc_file:
            acdc_json = json.loads(acdc_file.read())
            acdc_said = compact(acdc_json)

            if acdc_said not in ceg_acdc_saids:
                print(f'{acdc_path} cannot be verified.')

            markdown = acdc_json['a']['markdown']['values']
            assets = acdc_json['a']['assets']['values']

            markdown_filenames = [
                f
                for f in os.listdir(archive_directory)
                if f.endswith('.md') and os.path.isfile(os.path.join(archive_directory, f))
            ]

            for filename in markdown_filenames:
                if filename not in markdown:
                    print(f'{os.path.join(archive_directory, filename)} cannot be verified.')

            asset_filenames = [f for f in os.listdir(os.path.join(archive_directory, 'assets'))]

            for filename in asset_filenames:
                if filename not in assets:
                    print(f'{os.path.join(archive_directory, filename)} cannot be verified.')

            for markdown_path, markdown_details in markdown.items():
                path = os.path.join(archive_directory, markdown_path)
                with open(path, 'rb') as markdown_file:
                    diger = keri.core.coring.Diger(ser=markdown_file.read())
                    if diger.qb64 != markdown_details['digest']:
                        print(f'{path} cannot be verified.')

            for asset_path, asset_details in assets.items():
                path = os.path.join(archive_directory, 'assets', asset_path)
                with open(path, 'rb') as asset_file:
                    diger = keri.core.coring.Diger(ser=asset_file.read())
                    if diger.qb64 != asset_details['digest']:
                        print(f'{path} cannot be verified.')
