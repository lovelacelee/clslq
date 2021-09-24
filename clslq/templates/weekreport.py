wr_template = """

<html>

<head>
    <title>$title</title>
</head>
<style>
    .tablestyle {
        font-size: 11pt;
        font-family: Arial;
        border-collapse: collapse;
        border: 1px solid silver;
    }

    .tablestyle td {
        width: 300px;
    }

    .tablestyle td:nth-child(1) {
        width: 80px;
        text-align: center;
    }

    .tablestyle td:nth-child(3) {
        width: 60px;
        text-align: center;
    }

    .tablestyle td,
    th {
        padding: 5px;
    }

    .tablestyle tr:nth-child(even) {
        background: #E0E0E0;
    }

    .tablestyle th {
        background: #ff8936;
    }

    .tablestyle tr:hover {
        background: silver;
        cursor: pointer;
    }
</style>

<body>
    <table class="tablestyle">
        <thead>
            <th style="text-align: center; width: 1395px;">$title</th>
        </thead>
    </table>
    $table
    <table class="tablestyle">
        <thead>
            <th style="text-align: center; width: 1395px;">下周工作计划</th>
        </thead>
    </table>
    $plan
</body>

</html>


"""