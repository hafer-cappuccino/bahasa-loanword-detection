def test_dataset(wold_cldf):
    assert wold_cldf.module == 'Wordlist'
    assert wold_cldf.properties['dc:identifier'] == 'http://wold.clld.org'
