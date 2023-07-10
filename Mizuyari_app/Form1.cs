using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;


namespace Mizuyari_app
{
    public partial class watersprrinkler : Form
    {
        private int trackBar1_value_before = 0; // トラックバーの前回値
        public watersprrinkler()
        {
            InitializeComponent();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void progressBar1_Click(object sender, EventArgs e)
        {

        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
        
        }

        private void button1_Click(object sender, EventArgs e)
        {

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void exit_button_Click(object sender, EventArgs e)
        {
            MessageBox.Show("アプリケーションが終了されました");
            this.Close();
        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            {
                int diff = trackBar1.Value - trackBar1_value_before; // 前回との差分を計算

                textBox2.Text = (int.Parse(textBox2.Text) + diff).ToString(); // テキストボックスに差分を反映

                trackBar1_value_before = trackBar1.Value; // 前回の値を現在値で更新
            }

        }
        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            MessageBox.Show( "只今の湿度は"+ hum_textBox.Text +"%です" );
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            
        }

        private void trackBar2_Scroll(object sender, EventArgs e)
        {
           
         
        }

        private void radioButton3_CheckedChanged(object sender, EventArgs e)
        {

        }
    }
}