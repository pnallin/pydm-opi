#!/bin/bash
export PYTHONPATH=${PWD}
export HOME=${PWD}

# PV Gateway Address
export EPICS_CA_ADDR_LIST="\
\
10.0.38.34:5400 10.0.38.34:5402 10.0.38.34:5404 10.0.38.34:5406 10.0.38.34:5408 10.0.38.34:5410 10.0.38.34:5412 10.0.38.34:5414 10.0.38.34:5416 10.0.38.34:5418 \
10.0.38.34:5420 10.0.38.34:5422 10.0.38.34:5424 10.0.38.34:5426 10.0.38.34:5428 10.0.38.34:5430 10.0.38.34:5432 10.0.38.34:5434 10.0.38.34:5436 10.0.38.34:5438 \
10.0.38.34:5440 10.0.38.34:5442 10.0.38.34:5444 10.0.38.34:5446 10.0.38.34:5448 10.0.38.34:5450 10.0.38.34:5452 10.0.38.34:5454 10.0.38.34:5456 10.0.38.34:5458 \
10.0.38.34:5460 10.0.38.34:5462 10.0.38.34:5464 10.0.38.34:5466 10.0.38.34:5468 10.0.38.34:5470 10.0.38.34:5472 10.0.38.34:5474 10.0.38.34:5476 10.0.38.34:5478 \
10.0.38.34:5480 10.0.38.34:5482 10.0.38.34:5484 10.0.38.34:5486 10.0.38.34:5488 10.0.38.34:5490 10.0.38.34:5492 10.0.38.34:5494 10.0.38.34:5496 10.0.38.34:5498 \
10.0.38.34:5500 10.0.38.34:5502 10.0.38.34:5504 10.0.38.34:5506 10.0.38.34:5508 10.0.38.34:5510 10.0.38.34:5512 10.0.38.34:5514 10.0.38.34:5516 10.0.38.34:5518 \
10.0.38.34:5520 10.0.38.34:5522 10.0.38.34:5524 10.0.38.34:5526 10.0.38.34:5528 10.0.38.34:5530 10.0.38.34:5532 10.0.38.34:5534 10.0.38.34:5536 10.0.38.34:5538 \
10.0.38.34:5540 10.0.38.34:5542 10.0.38.34:5544 10.0.38.34:5546 10.0.38.34:5548 10.0.38.34:5550 10.0.38.34:5552 10.0.38.34:5554 10.0.38.34:5556 10.0.38.34:5558 \
10.0.38.34:5560 10.0.38.34:5562 10.0.38.34:5564 10.0.38.34:5566 10.0.38.34:5568 10.0.38.34:5570 10.0.38.34:5572 10.0.38.34:5574 10.0.38.34:5576 10.0.38.34:5578 \
10.0.38.34:5580 10.0.38.34:5582 10.0.38.34:5584 10.0.38.34:5586 10.0.38.34:5588 10.0.38.34:5590 10.0.38.34:5592 10.0.38.34:5594 10.0.38.34:5596 10.0.38.34:5598 \
10.0.38.34:5600 10.0.38.34:5602 10.0.38.34:5604 10.0.38.34:5606 10.0.38.34:5608 10.0.38.34:5610 10.0.38.34:5612 10.0.38.34:5614 10.0.38.34:5616 10.0.38.34:5618 \
10.0.38.34:5620 10.0.38.34:5622 10.0.38.34:5624 10.0.38.34:5626 10.0.38.34:5628 10.0.38.34:5630 10.0.38.34:5632 10.0.38.34:5634 10.0.38.34:5636 10.0.38.34:5638 \
10.0.38.34:5640 10.0.38.34:5642 10.0.38.34:5644 10.0.38.34:5646 10.0.38.34:5648 10.0.38.34:5650 10.0.38.34:5652 10.0.38.34:5654 10.0.38.34:5656 10.0.38.34:5658 \
10.0.38.34:5660 10.0.38.34:5662 10.0.38.34:5664 10.0.38.34:5666 10.0.38.34:5668 10.0.38.34:5670 10.0.38.34:5672 10.0.38.34:5674 10.0.38.34:5676 10.0.38.34:5678 \
10.0.38.34:5680 10.0.38.34:5682 10.0.38.34:5684 10.0.38.34:5686 10.0.38.34:5688 10.0.38.34:5690 10.0.38.34:5692 10.0.38.34:5694 10.0.38.34:5696 10.0.38.34:5698 \
10.0.38.34:5700 10.0.38.34:5702 10.0.38.34:5704 10.0.38.34:5706 10.0.38.34:5708 10.0.38.34:5710 10.0.38.34:5712 10.0.38.34:5714 10.0.38.34:5716 10.0.38.34:5718 \
10.0.38.34:5720 10.0.38.34:5722 10.0.38.34:5724 10.0.38.34:5726 10.0.38.34:5728 10.0.38.34:5730 10.0.38.34:5732 10.0.38.34:5734 10.0.38.34:5736 10.0.38.34:5738 \
10.0.38.34:5740 10.0.38.34:5742 10.0.38.34:5744 10.0.38.34:5746 10.0.38.34:5748 10.0.38.34:5750 10.0.38.34:5752 10.0.38.34:5754 10.0.38.34:5756 10.0.38.34:5758 \
10.0.38.34:5760 10.0.38.34:5762 10.0.38.34:5764 10.0.38.34:5766 10.0.38.34:5768 10.0.38.34:5770 10.0.38.34:5772 10.0.38.34:5774 10.0.38.34:5776 10.0.38.34:5778 \
10.0.38.34:5780 10.0.38.34:5782 10.0.38.34:5784 10.0.38.34:5786 10.0.38.34:5788 10.0.38.34:5790 10.0.38.34:5792 10.0.38.34:5794 10.0.38.34:5796 10.0.38.34:5798 \
10.0.38.34:5800 10.0.38.34:5802 10.0.38.34:5804 10.0.38.34:5806 10.0.38.34:5808 10.0.38.34:5810 10.0.38.34:5812 10.0.38.34:5814 10.0.38.34:5816 10.0.38.34:5818 \
10.0.38.34:5820 10.0.38.34:5822 10.0.38.34:5824 10.0.38.34:5826 10.0.38.34:5828 10.0.38.34:5830 10.0.38.34:5832 10.0.38.34:5834 10.0.38.34:5836 10.0.38.34:5838 \
10.0.38.34:5840 10.0.38.34:5842 10.0.38.34:5844 10.0.38.34:5846 10.0.38.34:5848 10.0.38.34:5850 10.0.38.34:5852 10.0.38.34:5854 10.0.38.34:5856 10.0.38.34:5858 \
10.0.38.34:5860 10.0.38.34:5862 10.0.38.34:5864 10.0.38.34:5866 10.0.38.34:5868 10.0.38.34:5870 10.0.38.34:5872 10.0.38.34:5874 10.0.38.34:5876 10.0.38.34:5878 \
"
# PYDM expects the following language setup
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

#OPTS="--hide-nav-bar --hide-menu-bar --hide-status-bar"
OPTS=""
pydm $OPTS src/launcher.py