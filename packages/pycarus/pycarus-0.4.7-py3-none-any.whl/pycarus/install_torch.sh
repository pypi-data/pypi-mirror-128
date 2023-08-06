echo '#### Downloading torch...'
wget -q --show-progress https://download.pytorch.org/whl/cu111/torch-1.9.1%2Bcu111-cp38-cp38-linux_x86_64.whl
echo '#### Installing torch...'
pip install torch*.whl
rm torch*.whl

echo '#### Downloading pytorch3d...'
wget -q --show-progress https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py38_cu111_pyt191/pytorch3d-0.6.0-cp38-cp38-linux_x86_64.whl
echo '#### Installing pytorch3d...'
pip install pytorch3d*.whl
rm pytorch3d*.whl
