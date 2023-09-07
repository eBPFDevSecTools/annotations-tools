set -x

#python3 comments_migration.py -s https://github.com/vbpf/ebpf-samples.git -c bd5009255d9aa6bdccb3f7057126fa005456aaab -r /tmp/ebpf-samples -o ../annotations/ -p ebpf-samples -i "/Users/palani/git/ebpf-projects-annotations/projects/ebpf-samples/human_annotated/ebpf-samples.db_comments.db"

#python3 comments_migration.py -s https://github.com/ebpf-networking/ebpf-ratelimiter.git -c ba0d5996651b74b0e995f4f535583db3b050b4c7 -r /tmp/ebpf-ratelimiter -o ../annotations/ -p ebpf-ratelimiter -i "/Users/palani/git/ebpf-projects-annotations/projects/rate-limiter/ebpf-ratelimiter_annotated.db"

#python3 comments_migration.py -s https://github.com/ebpf-networking/xdp-mptm.git -c b88a55de52a147fc1e3032af75d2036d0a3ba6fd -r /tmp/xdp-mptm -o ../annotations/ -p ebpf-xdp-mptm -i "/Users/palani/git/ebpf-projects-annotations/projects/mptm/xdp-mptm-main_annotated.db"


#python3 comments_migration.py -s https://github.com/ebpf-networking/bpf-filter.git -c ea73e8b45f4712766bd867079acc527b6fd98d68 -r /tmp/bpf-filter -o ../annotations/ -p bpf-filter -i "/Users/palani/git/ebpf-projects-annotations/projects/bpf-filter/bpf-filter_annotated.db"

#python3 comments_migration.py -s https://github.com/facebookincubator/katran.git -c b86858285509f473c5f5b7a0d04addc1f1ad1f55 -r /tmp/katran -o ../annotations/ -p katran -i "/Users/palani/git/ebpf-projects-annotations/projects/katran/katran_annotated.db"

#python3 comments_migration.py -s https://github.com/OISF/suricata.git -c 9353b07292255025069674df73b84acd88b254db -r /tmp/suricata -o ../annotations/ -p suricata -i "/Users/palani/git/ebpf-projects-annotations/projects/suricata-master/human_annotated/suricata-master.db_comments.db"

#python3 comments_migration.py -s https://github.com/cilium/cilium.git -c 8f606bafb696076609a01f88204d895576043950 -r /tmp/cilium -o ../annotations/ -p cilium -i "/Users/palani/git/ebpf-projects-annotations/projects/cilium/cilium_annotated.db"



#python3 comments_migration.py -s https://github.com/netobserv/netobserv-ebpf-agent.git -c e33e69016583da27507af47f4b09a9ca4538e406 -r /tmp/netobserv -o ../annotations/ -p netobserv -i "/Users/palani/git/ebpf-projects-annotations/projects/netobserv-bpf-main/human_annotated/netobserv-bpf-main.db_comments.db"


python3 comments_migration.py -s https://github.com/openshift/ingress-node-firewall.git -c 7bf8d11f60420be51488fca94d9469ecb4bd855c -r /tmp/ingress-node-firewall -o ../annotations/ -p ingress-node-firewall  -i "/Users/palani/git/ebpf-projects-annotations/projects/ingress-node-firewall-master/human_annotated/ingress-node-firewall-master.db_comments.db"



