#ifndef WFM_H
#define WFM_H

#include <QMainWindow>

namespace Ui {
class WFM;
}

class WFM : public QMainWindow
{
    Q_OBJECT

public:
    explicit WFM(QWidget *parent = 0);
    ~WFM();

private:
    Ui::WFM *ui;
};

#endif // WFM_H
