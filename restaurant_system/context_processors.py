def admin_settings(request):
    """
    添加管理后台通用设置到模板上下文
    """
    return {
        'site_title': '智能餐饮管理系统',
        'site_header': '智能餐饮管理系统',
        'has_add_permission': request.user.has_perm('add'),
        'has_change_permission': request.user.has_perm('change'),
        'has_delete_permission': request.user.has_perm('delete'),
    } 