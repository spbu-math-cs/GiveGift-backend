package com.example.givegift;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.view.View;
import android.widget.SeekBar;
import android.widget.TextView;

import java.util.LinkedList;
import java.util.List;

// Использовать Mediator
class Mediator {
    public static void seekBarListener(SeekBar seekBar, TextView textView) {
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean b) {
                textView.setText(String.valueOf(seekBar.getProgress() + progress));
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });
    }
}

class SeekBarListener {
    public void link(SeekBar seekBar1, SeekBar seekBar2, TextView textView1, TextView textView2) {
        Mediator.seekBarListener(seekBar1, textView1);
        Mediator.seekBarListener(seekBar2, textView2);
    }
}

public class MainActivity extends AppCompatActivity {

    @SuppressLint("DefaultLocale")
    public void create(List<String> gifts) {
        gifts.add(String.format("https://www.ozon.ru/product/karty-igralnye-plastikovye-54sht-dlya-pokera-skolzyashchie-pokernye-635858801/?advert=PtrTKtzjV23NV_As_D1KWe1L16Y7HFTe_yBNUa5E6M1aBkURH6LN-jMP_drE_7wZBadicN59prtSr9J-OETgGtfUdxJ-LwGHhAeOQDvdg01iGzNxizSdmXo8b5QLHS69PSVfXSIO4G62LyODnmsuFjxpnjVEuC0&avtc=1&avte=4&avts=1696236439 %d %d", 150, 300));
        gifts.add(String.format("https://www.ozon.ru/product/chay-travyanoy-listovoy-antistress-listovoy-100-gr-899392086/?advert=-rMWA92Vhjcr4ukDKYiFlYVuRj2cb-Q_2jEKUau_7-Fa4hQ2hWyrJnORi73crSAiRvPmzZcOAiCdndRAb2pQLaOc0oKCeimvZk2oZOmGNow57rk7GP1Gk_56vIL3XuBUfMCad-euZuKrTowPXBaK8sAeHE93Ds4oy9wdmA44L6zXGzTs7cBTBfjBcq3fvW2o5ghm&avtc=1&avte=2&avts=1696236439 %d %d", 300, 400));
        gifts.add(String.format("https://www.ozon.ru/product/sushilka-dlya-posudy-v-shkaf-60-sm-hrom-s-alyuminievoy-ramkoy-763543384/?advert=qjEn6mkqx-Cdt7BknN6mY4Cu_adLIKjx7Lli5iKOTt5rRvKLmL0dPVih0RWkS6BJbqrmNVMFA4jjA0AFR7recM67rXDkjHDj3BMVqSoNIeYgJtqu03Y6xDkQFeQpxdK-hePIxW5dXyRlqJndctbZJ_x8J372mKitpz6IMN7FVLGxK44cn62W00LRx8VN3PVfZXIl&avtc=1&avte=2&avts=1696236439 %d %d", 900, 1100));
        gifts.add(String.format("https://www.ozon.ru/product/nabor-instrumentov-dlya-avtomobilya-219-predmetov-306540667/?advert=ytSLGJuEr8giXosLcrQdXuHVE6Uop9GBegQ0SjJZGHTIlGe_uGHwYpPll-bx5ckYImdR1Wnbii2E7jL2oHN7KYCJYFZaqvNz043wkXrxYY_XMkBwCfQPHekzCs7xJjAnCDe3rWeftON8HYrkh4taPahaWHU1ZJGMayO-5j1zkljesA_UZRgg2cK8dkxSd2c-Iscn&avtc=1&avte=2&avts=1696236439 %d %d", 7000, 9000));
        gifts.add(String.format("https://www.ozon.ru/product/komplekt-iz-2h-mahrovyh-polotenets-30h70h2sht-unison-ritz-svetlo-zelenyy-487711916/?avtc=1&avte=2&avts=1696236439 %d %d", 200, 300));
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        SeekBar seekBar1 = findViewById(R.id.seekBar);
        SeekBar seekBar2 = findViewById(R.id.seekBar2);
        TextView leftPriceBorder = findViewById(R.id.leftPriceBorder);
        TextView rightPriceBorder = findViewById(R.id.rightPriceBorder);

        leftPriceBorder.setText(String.valueOf(seekBar1.getProgress()));
        rightPriceBorder.setText(String.valueOf(seekBar2.getProgress()));

        SeekBarListener seekBarListener = new SeekBarListener();
        seekBarListener.link(seekBar1, seekBar2, leftPriceBorder, rightPriceBorder);

        }

    public void search(View view) {
        SeekBar seekBar1 = findViewById(R.id.seekBar);
        SeekBar seekBar2 = findViewById(R.id.seekBar2);
        int min = seekBar1.getProgress();
        int max = seekBar2.getProgress();

        List<String> gifts = new LinkedList<>();
        String res = "";

        create(gifts);
        int i = 1;

        for (String s:
             gifts) {
            if (Integer.parseInt(s.split(" ")[1]) >= min && Integer.parseInt(s.split(" ")[2]) <= max) {
                res = res + i + ") " + s.split(" ")[0] + '\n';
                i++;
            }
        }

        TextView textView = findViewById(R.id.resultsSearch);
        textView.setText(res);
    }
}
