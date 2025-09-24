import sqlite3


TOOLS_LIST = {
    "function_declarations": [
        {
            "name": "get_crops_by_sellprice",
            "description": "根据季节、作物售价范围、成熟类型和排序方式检索农作物信息。该工具能够处理灵活的查询，并能按需返回特定数量的结果。",
            "parameters": {
                "type": "object",
                "properties": {
                    "season": {
                        "type": "string",
                        "description": "农作物的季节，如'春'、'夏'、'秋'或多个季节的组合（例如'春夏'）。如果未提供，则默认为所有季节。"
                    },
                    "min_price": {
                        "type": "integer",
                        "description": "农作物销售价格的最低值。如果只提供了最低价，则返回所有售价高于该价格的农作物。"
                    },
                    "max_price": {
                        "type": "integer",
                        "description": "农作物销售价格的最高值。如果只提供了最高价，则返回所有售价低于该价格的农作物。"
                    },
                    "grow_type": {
                        "type": "string",
                        "enum": ["单次", "连续"],
                        "description": "农作物的成熟类型。如果未提供，则返回所有类型。"
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["asc", "desc"],
                        "description": "结果根据作物售价的排序方向。'asc'为升序（从低到高），'desc'为降序（从高到低）。如果未提供，则按数据默认顺序返回。"
                    },
                    "top_n": {
                        "type": "integer",
                        "description": "要返回的前几项数据。如果未提供，则返回所有符合条件的记录。"
                    }
                },
                "required": []
            }
        },
        {
            "name": "get_crops_by_dailyrevenue",
            "description": "根据季节、每日利润范围、成熟类型和排序方式检索农作物信息。该工具能够处理灵活的查询，并能按需返回特定数量的结果。",
            "parameters": {
                "type": "object",
                "properties": {
                    "season": {
                        "type": "string",
                        "description": "农作物的季节，如'春'、'夏'、'秋'或多个季节的组合（例如'春夏'）。如果未提供，则默认为所有季节。"
                    },
                    "min_revenue": {
                        "type": "integer",
                        "description": "农作物每日利润的最低值。如果只提供了最低值，则返回所有每日利润高于该值的农作物。"
                    },
                    "max_revenue": {
                        "type": "integer",
                        "description": "农作物每日利润的最高值。如果只提供了最高值，则返回所有每日利润低于该值的农作物。"
                    },
                    "grow_type": {
                        "type": "string",
                        "enum": ["单次", "连续"],
                        "description": "农作物的成熟类型。如果未提供，则返回所有类型。"
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["asc", "desc"],
                        "description": "结果根据每日利润的排序方向。'asc'为升序（从低到高），'desc'为降序（从高到低）。如果未提供，则按数据默认顺序返回。"
                    },
                    "top_n": {
                        "type": "integer",
                        "description": "要返回的前几项数据。如果未提供，则返回所有符合条件的记录。"
                    }
                },
                "required": []
            }
        },
        {
            "name": "get_crops_by_seedprice",
            "description": "根据季节、种子价格范围、成熟类型和排序方式检索农作物信息。该工具能够处理灵活的查询，并能按需返回特定数量的结果。",
            "parameters": {
                "type": "object",
                "properties": {
                    "season": {
                        "type": "string",
                        "description": "农作物的季节，如'春'、'夏'、'秋'或多个季节的组合（例如'春夏'）。如果未提供，则默认为所有季节。"
                    },
                    "min_revenue": {
                        "type": "integer",
                        "description": "农作物种子售价的最低值。如果只提供了最低值，则返回所有种子售价高于该值的农作物。"
                    },
                    "max_revenue": {
                        "type": "integer",
                        "description": "农作物种子售价的最高值。如果只提供了最高值，则返回所有种子售价低于该值的农作物。"
                    },
                    "grow_type": {
                        "type": "string",
                        "enum": ["单次", "连续"],
                        "description": "农作物的成熟类型。如果未提供，则返回所有类型。"
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["asc", "desc"],
                        "description": "结果根据种子售价的排序方向。'asc'为升序（从低到高），'desc'为降序（从高到低）。如果未提供，则按数据默认顺序返回。"
                    },
                    "top_n": {
                        "type": "integer",
                        "description": "要返回的前几项数据。如果未提供，则返回所有符合条件的记录。"
                    }
                },
                "required": []
            }
        },
        {
            "name": "get_crops_by_growtime",
            "description": "根据季节、作物生长所需时间范围、成熟类型排序方式检索农作物信息。该工具能够处理灵活的查询，并能按需返回特定数量的结果。",
            "parameters": {
                "type": "object",
                "properties": {
                    "season": {
                        "type": "string",
                        "description": "农作物的季节，如'春'、'夏'、'秋'或多个季节的组合（例如'春夏'）。如果未提供，则默认为所有季节。"
                    },
                    "min_revenue": {
                        "type": "integer",
                        "description": "农作物生长所需时间的最低值。如果只提供了最低值，则返回所有生长所需时间高于该值的农作物。"
                    },
                    "max_revenue": {
                        "type": "integer",
                        "description": "农作物生长所需时间的最高值。如果只提供了最高值，则返回所有生长所需时间低于该值的农作物。"
                    },
                    "grow_type": {
                        "type": "string",
                        "enum": ["单次", "连续"],
                        "description": "农作物的成熟类型。如果未提供，则返回所有类型。"
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["asc", "desc"],
                        "description": "结果根据作物生长所需时间的排序方向。'asc'为升序（从低到高），'desc'为降序（从高到低）。如果未提供，则按数据默认顺序返回。"
                    },
                    "top_n": {
                        "type": "integer",
                        "description": "要返回的前几项数据。如果未提供，则返回所有符合条件的记录。"
                    }
                },
                "required": []
            }
        },
        {
            "name": "RAGCalling",
            "description": "若其他工具无法解决问题，则调用此函数来对RAG知识库检索获取信息。"
        },
    ]
}

# 根据售价范围获取对应季节的农作物
def get_crops_by_sellprice(season: str = None, min_price: int = None, max_price: int = None, grow_type: str = None, sort_by: str = None, top_n: int = None) -> str:
    print("calling get_crops_by_sellprice")
    with sqlite3.connect('stardewValley.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 构建动态SQL查询
        query = "SELECT * FROM crops WHERE 1=1"
        params = []

        if season is not None:
            query += " AND season LIKE ?"
            params.append(f"%{season}%")

        if min_price is not None and max_price is not None:
            query += " AND sell_price BETWEEN ? AND ?"
            params.append(min_price)
            params.append(max_price)
        elif min_price is not None:
            query += " AND sell_price >= ?"
            params.append(min_price)
        elif max_price is not None:
            query += " AND sell_price <= ?"
            params.append(max_price)

        if grow_type is not None:
            query += " AND grow_type = ?"
            params.append(grow_type)

        if sort_by:
            order = "ASC" if sort_by == "asc" else "DESC"
            query += f" ORDER BY sell_price {order}"

        if top_n is not None and top_n > 0:
            query += " LIMIT ?"
            params.append(top_n)

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

    if not results:
        return "未找到符合条件的作物。"

    output = "找到以下农作物:\n"
    for row in results:
        output += f"{row['name']}-季节:{row['season']}-种子来源:{row['seed_sell']}"
        if row['seed_sell'] != "非固定":
            output += f"-种子售价:{row['seed_price']}G"
        output += f"-作物基础售价:{row['sell_price']}G-收获种类:{row['grow_type']}收获-生长时间:{row['grow_time']}天"
        if row['grow_type'] == "连续":
            output += f"-收获间隔:{row['maturity_time']}天"
        output += f"-基础日均收益:{row['daily_revenue']}G\n"

    return output


# 根据每日收益范围获取对应季节的农作物
def get_crops_by_dailyrevenue(season: str = None, min_revenue: int = None, max_revenue: int = None, grow_type: str = None, sort_by: str = None, top_n: int = None) -> str:
    print("calling get_crops_by_dailyrevenue")
    with sqlite3.connect('stardewValley.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 构建动态SQL查询
        query = "SELECT * FROM crops WHERE 1=1"
        params = []

        if season is not None:
            query += " AND season LIKE ?"
            params.append(f"%{season}%")

        if min_revenue is not None and max_revenue is not None:
            query += " AND daily_revenue BETWEEN ? AND ?"
            params.append(min_revenue)
            params.append(max_revenue)
        elif min_revenue is not None:
            query += " AND daily_revenue >= ?"
            params.append(min_revenue)
        elif max_revenue is not None:
            query += " AND daily_revenue <= ?"
            params.append(max_revenue)

        if grow_type is not None:
            query += " AND grow_type = ?"
            params.append(grow_type)

        if sort_by:
            order = "ASC" if sort_by == "asc" else "DESC"
            query += f" ORDER BY daily_revenue {order}"

        if top_n is not None and top_n > 0:
            query += " LIMIT ?"
            params.append(top_n)

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

    if not results:
        return "未找到符合条件的作物。"

    output = "找到以下农作物:\n"
    for row in results:
        output += f"{row['name']}-季节:{row['season']}-种子来源:{row['seed_sell']}"
        if row['seed_sell'] != "非固定":
            output += f"-种子售价:{row['seed_price']}G"
        output += f"-作物基础售价:{row['sell_price']}G-收获种类:{row['grow_type']}收获-生长时间:{row['grow_time']}天"
        if row['grow_type'] == "连续":
            output += f"-收获间隔:{row['maturity_time']}天"
        output += f"-基础日均收益:{row['daily_revenue']}G\n"

    return output

# 根据种子价格范围获取对应季节的农作物
def get_crops_by_seedprice(season: str = None, min_price: int = None, max_price: int = None, grow_type: str = None, sort_by: str = None, top_n: int = None) -> str:
    print("calling get_crops_by_seedprice")
    with sqlite3.connect('stardewValley.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 构建动态SQL查询
        query = "SELECT * FROM crops WHERE 1=1"
        params = []

        if season is not None:
            query += " AND season LIKE ?"
            params.append(f"%{season}%")

        if min_price is not None and max_price is not None:
            query += " AND seed_price BETWEEN ? AND ?"
            params.append(min_price)
            params.append(max_price)
        elif min_price is not None:
            query += " AND seed_price >= ?"
            params.append(min_price)
        elif max_price is not None:
            query += " AND seed_price <= ?"
            params.append(max_price)

        if grow_type is not None:
            query += " AND grow_type = ?"
            params.append(grow_type)

        if sort_by:
            order = "ASC" if sort_by == "asc" else "DESC"
            query += f" ORDER BY seed_price {order}"

        if top_n is not None and top_n > 0:
            query += " LIMIT ?"
            params.append(top_n)

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

    if not results:
        return "未找到符合条件的作物。"

    output = "找到以下农作物:\n"
    for row in results:
        output += f"{row['name']}-季节:{row['season']}-种子来源:{row['seed_sell']}"
        if row['seed_sell'] != "非固定":
            output += f"-种子售价:{row['seed_price']}G"
        output += f"-作物基础售价:{row['sell_price']}G-收获种类:{row['grow_type']}收获-生长时间:{row['grow_time']}天"
        if row['grow_type'] == "连续":
            output += f"-收获间隔:{row['maturity_time']}天"
        output += f"-基础日均收益:{row['daily_revenue']}G\n"

    return output


# 根据作物生长时间范围获取对应季节的农作物
def get_crops_by_growtime(season: str = None, min_growtime: int = None, max_growtime: int = None, grow_type: str = None, sort_by: str = None, top_n: int = None) -> str:
    print("calling get_crops_by_seedprice")
    with sqlite3.connect('stardewValley.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 构建动态SQL查询
        query = "SELECT * FROM crops WHERE 1=1"
        params = []

        if season is not None:
            query += " AND season LIKE ?"
            params.append(f"%{season}%")

        if min_growtime is not None and max_growtime is not None:
            query += " AND grow_time BETWEEN ? AND ?"
            params.append(min_growtime)
            params.append(max_growtime)
        elif min_growtime is not None:
            query += " AND grow_time >= ?"
            params.append(min_growtime)
        elif max_growtime is not None:
            query += " AND grow_time <= ?"
            params.append(max_growtime)

        if grow_type is not None:
            query += " AND grow_type = ?"
            params.append(grow_type)

        if sort_by:
            order = "ASC" if sort_by == "asc" else "DESC"
            query += f" ORDER BY grow_time {order}"

        if top_n is not None and top_n > 0:
            query += " LIMIT ?"
            params.append(top_n)

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

    if not results:
        return "未找到符合条件的作物。"

    output = "找到以下农作物:\n"
    for row in results:
        output += f"{row['name']}-季节:{row['season']}-种子来源:{row['seed_sell']}"
        if row['seed_sell'] != "非固定":
            output += f"-种子售价:{row['seed_price']}G"
        output += f"-作物基础售价:{row['sell_price']}G-收获种类:{row['grow_type']}收获-生长时间:{row['grow_time']}天"
        if row['grow_type'] == "连续":
            output += f"-收获间隔:{row['maturity_time']}天"
        output += f"-基础日均收益:{row['daily_revenue']}G\n"

    return output