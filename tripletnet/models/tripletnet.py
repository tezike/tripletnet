# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/tripletnet.ipynb (unless otherwise specified).

__all__ = ['TripletNet']

# Cell
import torch
import torch.nn as nn
import torch.nn.functional as F

# Cell
class TripletNet(nn.Module):
    def __init__(self, embeddingnet):
        super(TripletNet, self).__init__()
        self.embeddingnet = conditionalnet

    def forward(self, q, p, n, c):
        """
        q: Query Image
        p: Positive Image
        n: Negative Image
        c: Condition of similarity
        """

        # it is important to normalize the embeddings while using triplets
        embedded_x, masknorm_norm_q, embed_norm_q, tot_embed_norm_q = self.conditionalnet(q, c)
        embedded_p, masknorm_norm_p, embed_norm_p, tot_embed_norm_p = self.conditionalnet(p, c)
        embedded_n, masknorm_norm_n, embed_norm_n, tot_embed_norm_n = self.conditionalnet(n, c)
        mask_norm = (masknorm_norm_q + masknorm_norm_p + masknorm_norm_n) / 3
        embed_norm = (embed_norm_q + embed_norm_p + embed_norm_n) / 3
        mask_embed_norm = (tot_embed_norm_q + tot_embed_norm_p + tot_embed_norm_n) / 3

        pos_dist = F.pairwise_distance(embedded_q, embedded_p, 2)
        neg_dist = F.pairwise_distance(embedded_q, embedded_n, 2)

        return pos_dist, neg_dist, mask_norm, embed_norm, mask_embed_norm