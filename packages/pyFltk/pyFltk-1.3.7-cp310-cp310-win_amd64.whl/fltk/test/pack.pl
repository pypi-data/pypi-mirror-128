#!/usr/bin/perl
use pmfltk;

$window = Fl_Window->new(365, 525, "$0");
$scroll = Fl_Scroll->new(10, 10, 345, 285);
$scroll->box(5);
$pack = Fl_Pack->new(10, 10, 345, 285);
$pack->box(5);
@button = 0;
$x = 35;
$y = 0;
while ($y < 24) {
	$o = $y + 1;
	$button[$y] = Fl_Button->new( $x, $x, 25, 25, "b$o");
	$x = $x + 10;
	$y++;
}
$pack->end();
$window->resizable($pack);
$scroll->end();
$horiz = Fl_Radio_Light_Button->new(10, 325, 175, 25, "HORIZONTAL");
$horiz->pmCallback("horiz_cb");
$horiz->value(1);
$horiz->labeltype(FL_EMBOSSED_LABEL);
$vert = Fl_Radio_Light_Button->new(10, 350, 175, 25, "VERTICAL");
$vert->pmCallback("vert_cb");
$slider = Fl_Hor_Value_Slider->new(55, 375, 295, 25, "spacing:");
$slider->range(0, 30);
$slider->align(4);
$slider->step(1);
$slider->pmCallback("slider_cb");
$window->end();
$window->show();
pmfltk::FlRun();

sub horiz_cb {
	for ($i = 0; $i < $pack->children(); $i++) {
	  $button[$i]->resize(0, 0, 25, 25);
	}
	$pack->resize($scroll->x(), $scroll->y(), $scroll->w(), $scroll->h());
	$pack->parent()->redraw();
	$pack->type(0);
	$pack->redraw();
}

sub vert_cb {
        for ($i = 0; $i < $pack->children(); $i++) {
          $button[$i]->resize(0, 0, 25, 25);
        }
        $pack->resize($scroll->x(), $scroll->y(), $scroll->w(), $scroll->h());
        $pack->parent()->redraw();
        $pack->type(1);
        $pack->redraw();
}

sub slider_cb {
	$val = $slider->value();
	$pack->spacing($val);
	$scroll->redraw();
}
