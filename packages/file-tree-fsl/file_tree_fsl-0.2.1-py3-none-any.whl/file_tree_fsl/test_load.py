from file_tree import FileTree, parse_tree

def test_load_all():
    """Loads all the sub-trees stored in file-tree to check for formatting errors
    """
    for key in parse_tree.available_subtrees:
        tree = FileTree.read(key)
        assert len(tree.template_keys()) > 1


def test_load_list():
    for key in [
        'bedpostx',
        'BedpostX',
        'bet', 
        'bids_raw',
        'diffusion',
        'Diffusion',
        'dti',
        'eddy',
        'epi_reg',
        'fast',
        'feat_reg',
        'feat_stats',
        'feat',
        'freesurfer',
        'fsl_anat',
        'gfeat',
        'HCP_directory',
        'HCP_surface',
        'HCP_Surface',
        'probtrackx',
        'ProbtrackX',
        'tbss',
        'topup',
        'vbm'
    ]:
        FileTree.read(key)