from flask import jsonify
from flask_jwt_extended import JWTManager
from ..commons import IdentityFormater, exceptions


jwt = JWTManager()


@jwt.user_loader_callback_loader
def user_loader_handler(identity):
    from ..models import Role
    login_name, login_role = IdentityFormater.load(identity)
    account_model = Role.MODELS[login_role]
    return account_model.query.filter_by(login_name=login_name).first()


@jwt.user_loader_error_loader
def user_loader_error_handler(msg):
    exception = exceptions.AccountLoadError()
    return jsonify(exception.to_dict()), exception.http_code


@jwt.expired_token_loader
def expired_token_handler():
    exception = exceptions.JWTExpiredTokenError()
    return jsonify(exception.to_dict()), exception.http_code


@jwt.invalid_token_loader
def invalid_token_handler(msg):
    exception = exceptions.JWTInvalidTokenError()
    return jsonify(exception.to_dict()), exception.http_code


@jwt.unauthorized_loader
def unauthorized_handler(msg):
    exception = exceptions.JWTUnauthorizedError()
    return jsonify(exception.to_dict()), exception.http_code


@jwt.revoked_token_loader
def revoked_token_handler():
    exception = exceptions.JWTRevokedTokenError()
    return jsonify(exception.to_dict()), exception.http_code


@jwt.needs_fresh_token_loader
def needs_fresh_token_handler():
    exception = exceptions.JWTNeedsFreshTokenError()
    return jsonify(exception.to_dict()), exception.http_code


# @jwt.claims_verification_failed_loader
# def claims_verification_failed_handler():
#     exception = exceptions.JWTClaimsVerificationFailed()
#     return jsonify(exception.to_dict()), exception.http_code
