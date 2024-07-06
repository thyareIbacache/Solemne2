const express = require('express');
const bodyParser = require('body-parser');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 8000;

const pool = new Pool({
    user: 'tu_usuario',
    host: 'localhost',
    database: 'tu_base_de_datos',
    password: 'tu_contraseña',
    port: 5432
});

app.use(bodyParser.json());
app.use(cors());

app.get('/api/archivos', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM archivos WHERE estado = \'pendiente\' ORDER BY fecha_carga DESC');
        res.json(result.rows);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error al obtener los archivos');
    }
});

app.post('/api/archivos/:id/aprobar', async (req, res) => {
    const { id } = req.params;
    try {
        const result = await pool.query('UPDATE archivos SET estado = \'aprobado\' WHERE id = $1 RETURNING *', [id]);
        res.status(200).json(result.rows[0]);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error al aprobar el archivo');
    }
});

app.post('/api/archivos/:id/rechazar', async (req, res) => {
    const { id } = req.params;
    try {
        const result = await pool.query('UPDATE archivos SET estado = \'rechazado\' WHERE id = $1 RETURNING *', [id]);
        res.status(200).json(result.rows[0]);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error al rechazar el archivo');
    }
});

app.listen(port, () => {
    console.log(`Servidor corriendo en http://localhost:${port}`);
});
