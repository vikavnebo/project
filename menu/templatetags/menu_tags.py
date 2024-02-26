from django import template

from menu.models import Item


register = template.Library()


def is_selected(item, url):
    return item.url == url


def is_child(item, selected_item):
    return item.parent_id == selected_item.id


def is_parent(item, selected_item):
    return item.id == selected_item.parent_id


def is_primary(item, exclude_id=None):
    return item.parent_id is None and item.id != exclude_id


def get_items_for_display(selected_item, all_items):
    items_for_display = list()
    current_item = selected_item

    if not current_item:
        return list(filter(is_primary, all_items))

    while current_item:
        children = list(filter(lambda item: is_child(item, current_item), all_items))

        current_item.children = children

        if is_primary(current_item):
            items_for_display.append(current_item)
            items_for_display.extend(
                                    list(
                                        filter(
                                                lambda item: is_primary(item, current_item.id),
                                                all_items)
                                        )
                                    )
            break

        current_item = next(
                            iter(
                                list(
                                    filter(
                                        lambda item: is_parent(item, current_item),
                                        all_items)
                                    )
                                ), None
                            )

    return items_for_display


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_url):
    result = {}
    all_items = list(Item.used.filter(menu__url=menu_url))
    selected_item_url = context['request'].path[1:-1]
    result['selected_item'] = next(
                                    iter(
                                        list(
                                            filter(
                                                lambda item: is_selected(item, selected_item_url),
                                                all_items)
                                            )
                                        ), None
                                    )
    result['items_for_display'] = sorted(get_items_for_display(result['selected_item'], all_items),
                                         key=lambda item: item.id)
    return result
