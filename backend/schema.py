import graphene

from graphene_django.debug import DjangoDebug

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

import backend.Apps.account.queries
import backend.Apps.account.mutations
import backend.Apps.user.queries
import backend.Apps.user.mutations
import backend.Apps.product.queries
import backend.Apps.product.mutations


class AuthMutation(graphene.ObjectType):

    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation =  mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()
    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()




class Query(
        backend.Apps.account.queries.Query,
        backend.Apps.user.queries.Query,
        backend.Apps.product.queries.Query,
        UserQuery, MeQuery, 
        graphene.ObjectType):
    
    debug = graphene.Field(DjangoDebug, name="_debug")



class Mutation(
        backend.Apps.account.mutations.Mutation,
        backend.Apps.user.mutations.Mutation,
        backend.Apps.product.mutations.Mutation,
        AuthMutation, 
        graphene.ObjectType):
    
    pass


schema = graphene.Schema(
    query=Query, mutation=Mutation)
